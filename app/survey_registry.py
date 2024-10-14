# app/survey_registry.py

from typing import Dict
from .surveys.shs import SHSSurvey
from .surveys.stress import StressSurvey
from .models import SurveyBase

survey_registry: Dict[int, SurveyBase] = {
    1: SHSSurvey(),
    2: StressSurvey(),
    # Add new surveys here
}
