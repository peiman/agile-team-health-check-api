# app/survey_registry.py

from typing import Dict, List
from .surveys.shs import SHSSurvey
from .surveys.stress import StressSurvey
from .models import SurveyBase


class SurveyRegistry:
    """
    Registry for managing surveys.
    """

    def __init__(self):
        self._surveys: Dict[int, SurveyBase] = {}

    def register_survey(self, survey: SurveyBase):
        self._surveys[survey.id] = survey

    def get_survey(self, survey_id: int) -> SurveyBase:
        return self._surveys.get(survey_id)

    def list_surveys(self) -> List[SurveyBase]:
        return list(self._surveys.values())


# Instantiate the registry and register surveys
SurveyRegistry = SurveyRegistry()
SurveyRegistry.register_survey(SHSSurvey())
SurveyRegistry.register_survey(StressSurvey())
