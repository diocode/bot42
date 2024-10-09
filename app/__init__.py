<<<<<<< Updated upstream
# Marks dir as a Python Package
from . import api, printer, slack_bot

__all__ = [
  "api",
  "printer",
  "slack_bot",
=======
from .api import get_42_api_token, validate_student, get_student_data, get_piscine_data
from .slack_bot import app, get_student, get_piscine
from .printer import format_student_info

__all__ = [
    "app",
    "get_42_api_token",
    "get_student_data",
    "validate_student",
    "get_piscine_data",
    "app",
    "get_student",
    "get_piscine",
    "format_student_info",
>>>>>>> Stashed changes
]
