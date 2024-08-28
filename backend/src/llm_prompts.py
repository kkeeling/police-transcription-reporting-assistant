"""
This module contains system and user prompts for LLMs used in police report generation.
"""

import os
import llm

# Load system prompt from file
current_dir = os.path.dirname(os.path.abspath(__file__))
system_prompt_path = os.path.join(current_dir, 'SYSTEM_PROMPT.md')
user_prompt_path = os.path.join(current_dir, 'USER_PROMPT.md')
example_report_path = os.path.join(current_dir, 'example_report.md')

with open(system_prompt_path, 'r') as file:
    POLICE_REPORT_SYSTEM_PROMPT = file.read().strip()

with open(user_prompt_path, 'r') as file:
    POLICE_REPORT_USER_PROMPT_TEMPLATE = file.read().strip()

with open(example_report_path, 'r') as file:
    EXAMPLE_REPORT = file.read().strip()

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
    
    return POLICE_REPORT_USER_PROMPT_TEMPLATE.format(
        transcription=transcription,
        reportType=report_type,
        example_report=EXAMPLE_REPORT
    )

def generate_report(transcription: str, report_type: str, model_name: str = "llama2") -> str:
    """
    Generate a police report using the specified LLM model.

    Args:
        transcription (str): The transcribed audio content.
        report_type (str): The type of report to generate.
        model_name (str): The name of the model to use.

    Returns:
        str: The generated police report.
    """
    user_prompt = generate_user_prompt(transcription, report_type)
    
    try:
        model = llm.get_model(model_name)
        response = model.prompt(user_prompt, system=POLICE_REPORT_SYSTEM_PROMPT)
        return response.text()
    except llm.UnknownModelError:
        raise ValueError(f"Unknown model: {model_name}")

def get_available_models() -> list:
    """
    Get a list of available LLM models.

    Returns:
        list: A list of available model names.
    """
    return [model.name for model in llm.models()]
