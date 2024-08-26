"""
This module contains system and user prompts for LLMs used in police report generation.
"""

import os

# Load system prompt from file
current_dir = os.path.dirname(os.path.abspath(__file__))
system_prompt_path = os.path.join(current_dir, 'SYSTEM_PROMPT.md')
user_prompt_path = os.path.join(current_dir, 'USER_PROMPT.md')

with open(system_prompt_path, 'r') as file:
    POLICE_REPORT_SYSTEM_PROMPT = file.read().strip()

with open(user_prompt_path, 'r') as file:
    POLICE_REPORT_USER_PROMPT_TEMPLATE = file.read().strip()

def generate_user_prompt(transcription: str, report_type: str) -> str:
    """
    Generate a user prompt for police report generation based on the given transcription.

    Args:
        transcription (str): The transcribed audio content.
        reportType (str): The type of report to generate.

    Returns:
        str: The formatted user prompt with the transcription inserted.
    """
    return POLICE_REPORT_USER_PROMPT_TEMPLATE.format(transcription=transcription, reportType=reportType)
