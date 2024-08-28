"""
This module contains system and user prompts for LLMs used in police report generation.
"""

import os
import llm
from chain import FusionChain
from typing import List, Dict, Any

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

def evaluator(outputs: List[str]) -> tuple[str, List[float]]:
    """
    Stub for the evaluator function.
    This function will be implemented later to evaluate and score the outputs from different models.

    Args:
        outputs (List[str]): List of outputs from different models.

    Returns:
        tuple[str, List[float]]: A tuple containing the top response and a list of scores for each output.
    """
    # For now, we'll just return the first output as the top response and equal scores for all outputs
    return outputs[0], [1.0] * len(outputs)

def generate_report(transcription: str, report_type: str) -> str:
    """
    Generate a police report using FusionChain with multiple LLM models.

    Args:
        transcription (str): The transcribed audio content.
        report_type (str): The type of report to generate.

    Returns:
        str: The generated police report.
    """
    user_prompt = generate_user_prompt(transcription, report_type)
    
    # Create models
    models = [
        llm.get_model("gemma2"),
        llm.get_model("llama3.1"),
        llm.get_model("mistral")
    ]

    def prompt_model(model: Any, prompt: str) -> str:
        return model.prompt(prompt, system=POLICE_REPORT_SYSTEM_PROMPT).text()

    result = FusionChain.run(
        context={"user_prompt": user_prompt},
        models=models,
        callable=prompt_model,
        prompts=["{{user_prompt}}"],
        evaluator=evaluator,
        get_model_name=lambda model: model.model_id
    )

    return result.top_response

def get_available_models() -> list:
    """
    Get a list of available LLM models.

    Returns:
        list: A list of available model names.
    """
    return [model.name for model in llm.models()]
