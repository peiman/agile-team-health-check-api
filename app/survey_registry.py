# app/survey_registry.py

from typing import Dict, List, Optional
from .surveys.shs import SHSSurvey
from .surveys.stress import StressSurvey
from .models import SurveyBase


class SurveyRegistry:
    """
    Registry for managing surveys.
    """

    def __init__(self) -> None:
        self._surveys: Dict[int, SurveyBase] = {}

    def register_survey(self, survey: SurveyBase) -> None:
        self._surveys[survey.id] = survey

    def get_survey(self, survey_id: int) -> Optional[SurveyBase]:
        return self._surveys.get(survey_id)

    def list_surveys(self) -> List[SurveyBase]:
        return list(self._surveys.values())


# Instantiate the registry and register surveys
survey_registry = SurveyRegistry()
survey_registry.register_survey(SHSSurvey())
survey_registry.register_survey(StressSurvey())
