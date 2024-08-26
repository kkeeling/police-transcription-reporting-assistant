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
        report_type (str): The type of report to generate. Must be either "General Occurrence" or "Crown Brief".

    Returns:
        str: The formatted user prompt with the transcription inserted.

    Raises:
        ValueError: If an invalid report_type is provided.
    """
    valid_report_types = ["General Occurrence", "Crown Brief"]
    if report_type not in valid_report_types:
        raise ValueError(f"Invalid report_type. Must be one of: {', '.join(valid_report_types)}")
    
    return POLICE_REPORT_USER_PROMPT_TEMPLATE.format(transcription=transcription, report_type=report_type)
