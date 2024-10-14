# models.py

from typing import List
from pydantic import BaseModel
from datetime import datetime

class Question(BaseModel):
    id: int
    text: str
    category: str

class Answer(BaseModel):
    question_id: int
    score: int  # Score from 1 to 5

class Response(BaseModel):
    id: int
    answers: List[Answer]
    timestamp: datetime
