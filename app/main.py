# app/main.py

import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import List
from .models import ResponseBase, AssessmentResultBase, QuestionBase, AnswerBase
from .survey_registry import survey_registry
from .repositories.assessment_repository import AssessmentRepository
from .exceptions import InvalidAnswerException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()
assessment_repository = AssessmentRepository()

@app.exception_handler(InvalidAnswerException)
async def invalid_answer_exception_handler(request: Request, exc: InvalidAnswerException):
    logger.error(f"InvalidAnswerException: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message},
    )

@app.get("/surveys/{survey_id}/questions", response_model=List[QuestionBase])
async def get_survey_questions(survey_id: int):
    logger.info(f"Fetching questions for survey_id: {survey_id}")
    survey = survey_registry.get(survey_id)
    if not survey:
        logger.error(f"Survey with ID {survey_id} not found.")
        raise HTTPException(status_code=404, detail="Survey not found")
    return survey.questions

@app.post("/surveys/{survey_id}/responses", response_model=AssessmentResultBase)
async def submit_survey_response(survey_id: int, response: ResponseBase, request: Request):
    logger.info(f"Submitting response for survey_id: {survey_id} from {request.client.host}")
    survey = survey_registry.get(survey_id)
    if not survey:
        logger.error(f"Survey with ID {survey_id} not found.")
        raise HTTPException(status_code=404, detail="Survey not found")

    # Validate that all required questions have been answered
    required_question_ids = {q.id for q in survey.questions}
    answered_question_ids = {a.question_id for a in response.answers}
    if required_question_ids != answered_question_ids:
        missing_questions = required_question_ids - answered_question_ids
        logger.error(f"Incomplete set of answers. Missing questions: {missing_questions}")
        raise HTTPException(status_code=400, detail=f"Incomplete set of answers. Missing questions: {missing_questions}")

    # Validate answers
    for answer in response.answers:
        question = next((q for q in survey.questions if q.id == answer.question_id), None)
        if not question:
            logger.error(f"Invalid question ID {answer.question_id} in response.")
            raise InvalidAnswerException(f"Invalid question ID {answer.question_id}.")
        if not (question.scale_min <= answer.score <= question.scale_max):
            logger.error(f"Score for question ID {answer.question_id} must be between {question.scale_min} and {question.scale_max}.")
            raise InvalidAnswerException(
                f"Score for question ID {answer.question_id} must be between {question.scale_min} and {question.scale_max}."
            )

    # Calculate scores
    scores = survey.scoring_mechanism.calculate_score(response.answers, survey.questions)
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
