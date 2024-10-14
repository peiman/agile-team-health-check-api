# main.py

from fastapi import FastAPI, HTTPException
from typing import List
from datetime import datetime
import logging

from models import Question, Response, Answer

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sample data storage (in-memory)
questions_db = [
    Question(id=1, text="How do you rate team communication?", category="Communication"),
    Question(id=2, text="Are sprint goals clear?", category="Clarity"),
    # Add more questions as needed
]

responses_db = []

# Endpoint to get all questions
@app.get("/questions", response_model=List[Question])
async def get_questions():
    logger.info("Fetching all questions")
    return questions_db

# Endpoint to submit responses
@app.post("/responses", response_model=Response, status_code=201)
async def submit_response(answers: List[Answer]):
    logger.info(f"Submitting response with {len(answers)} answers")
    response_id = len(responses_db) + 1
    response = Response(
        id=response_id,
        answers=answers,
        timestamp=datetime.utcnow()
    )
    responses_db.append(response)
    return response

# Endpoint to get a specific response
@app.get("/responses/{response_id}", response_model=Response)
async def get_response(response_id: int):
    logger.info(f"Fetching response with ID {response_id}")
    for response in responses_db:
        if response.id == response_id:
            return response
    logger.error(f"Response with ID {response_id} not found")
    raise HTTPException(status_code=404, detail="Response not found")
