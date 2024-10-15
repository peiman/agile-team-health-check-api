# app/main.py

import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List, Dict
from .models import (
    ResponseBase,
    AssessmentResultBase,
    QuestionBase,
    SurveyModel,
    SurveySummary,
)
from .survey_registry import survey_registry
from .repositories.assessment_repository import AssessmentRepository
from .exceptions import InvalidAnswerException

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create the FastAPI app with metadata
app = FastAPI(
    title="Agile Team Health Check API",
    description="An API for measuring and visualizing the health of Agile teams using survey instruments.",  # noqa
    version="0.1.0",
    contact={
        "name": "Peiman Khorramshahi",
        "url": "https://peiman.se",
        "email": "peiman@khorramshahi.com",
    },
)

assessment_repository = AssessmentRepository()


@app.exception_handler(InvalidAnswerException)
async def invalid_answer_exception_handler(
    request: Request, exc: InvalidAnswerException
) -> JSONResponse:
    logger.error(f"InvalidAnswerException: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )


@app.get("/", summary="Root Greeting", tags=["General"])
async def root() -> Dict[str, str]:
    """
    Returns a simple greeting message.

    - **Returns**: A greeting message as a dictionary.
    """
    return {"message": "Hello agile team"}


@app.get(
    "/surveys/",
    response_model=List[SurveySummary],
    summary="Get List of Surveys",
    tags=["Surveys"],
)
async def list_surveys() -> List[SurveySummary]:
    """
    Retrieve a list of all available surveys.

    - **Returns**: A list of surveys with their IDs, names, and types.
    """
    logger.info("Fetching list of all surveys")
    survey_summaries = [
        SurveySummary(id=survey.id, name=survey.name, survey_type=survey.survey_type)
        for survey in survey_registry.list_surveys()
    ]
    return survey_summaries


@app.get(
    "/surveys/{survey_id}",
    response_model=SurveyModel,
    summary="Get Survey Details",
    tags=["Surveys"],
)
async def get_survey_details(survey_id: int) -> SurveyModel:
    """
    Retrieve the details of a given survey, including its questions.

    - **survey_id**: The ID of the survey.
    - **Returns**: The survey details.
    """
    logger.info(f"Fetching details for survey_id: {survey_id}")
    survey = survey_registry.get_survey(survey_id)
    if not survey:
        logger.error(f"Survey with ID {survey_id} not found.")
        raise HTTPException(status_code=404, detail="Survey not found")
    # Convert SurveyBase instance to SurveyModel
    survey_model = SurveyModel(
        id=survey.id,
        name=survey.name,
        survey_type=survey.survey_type,
        questions=survey.questions,
    )
    return survey_model


@app.get(
    "/surveys/{survey_id}/questions",
    response_model=List[QuestionBase],
    summary="Get Survey Questions",
    tags=["Surveys"],
)
async def get_survey_questions(survey_id: int) -> List[QuestionBase]:
    """
    Retrieve the list of questions for a given survey.

    - **survey_id**: The ID of the survey.
    - **Returns**: A list of questions with their details.
    """
    logger.info(f"Fetching questions for survey_id: {survey_id}")
    survey = survey_registry.get_survey(survey_id)
    if not survey:
        logger.error(f"Survey with ID {survey_id} not found.")
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey.questions


@app.post(
    "/surveys/{survey_id}/responses",
    response_model=AssessmentResultBase,
    summary="Submit Survey Response",
    tags=["Surveys"],
)
async def submit_survey_response(
    survey_id: int, response: ResponseBase, request: Request
) -> AssessmentResultBase:
    """
    Submit responses for a survey and receive the calculated assessment result.

    - **survey_id**: The ID of the survey.
    - **response**: The survey responses submitted by the user.
    - **Returns**: The assessment result including calculated scores.
    """
    client_host = request.client.host if request.client else "Unknown"
    logger.info(f"Submitting response for survey_id: {survey_id} from {client_host}")
    survey = survey_registry.get_survey(survey_id)
    if not survey:
        logger.error(f"Survey with ID {survey_id} not found.")
        raise HTTPException(status_code=404, detail="Survey not found")

    # Validate that all required questions have been answered
    required_question_ids = {q.id for q in survey.questions}
    answered_question_ids = {a.question_id for a in response.answers}
    if required_question_ids != answered_question_ids:
        missing_questions = required_question_ids - answered_question_ids
        logger.error(
            f"Incomplete set of answers. Missing questions: {missing_questions}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Incomplete set of answers. Missing questions: {missing_questions}",
        )

    # Validate answers
    for answer in response.answers:
        question = next(
            (q for q in survey.questions if q.id == answer.question_id), None
        )
        if not question:
            logger.error(f"Invalid question ID {answer.question_id} in response.")
            raise InvalidAnswerException(f"Invalid question ID {answer.question_id}.")
        if not (question.scale_min <= answer.score <= question.scale_max):
            logger.error(
                f"Score for question ID {answer.question_id} must be between "
                f"{question.scale_min} and {question.scale_max}."
            )
            raise InvalidAnswerException(
                f"Score for question ID {answer.question_id} must be between "
                f"{question.scale_min} and {question.scale_max}."
            )

    # Calculate scores
    scores = survey.scoring_mechanism.calculate_score(
        response.answers, survey.questions
    )
    logger.debug(f"Calculated scores: {scores}")

    # Create assessment result
    assessment = AssessmentResultBase(
        id=0,  # ID will be set by repository
        survey_id=survey_id,
        scores=scores,
        timestamp=response.timestamp,
    )
    saved_assessment = assessment_repository.save(assessment)
    logger.info(f"Assessment {saved_assessment.id} saved successfully.")
    return saved_assessment
