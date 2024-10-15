# app/scoring.py

from abc import ABC, abstractmethod
from typing import Dict, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .models import AnswerBase, QuestionBase


class ScoringMechanism(ABC):
    @abstractmethod
    def calculate_score(
        self, answers: List["AnswerBase"], questions: List["QuestionBase"]
    ) -> Dict[str, float]:
        pass
