"""
This module contains system and user prompts for LLMs used in police report generation.
"""

import os
from dotenv import load_dotenv
import llm
from .chain import FusionChain
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
    Evaluate the outputs from different models and return the one most similar to the example report format.

    Args:
        outputs (List[str]): List of outputs from different models.

    Returns:
        tuple[str, List[float]]: A tuple containing the top response and a list of scores for each output.
    """
    with open(example_report_path, 'r') as file:
        example_report = file.read().strip()

    scores = []
    for output in outputs:
        # Calculate a simple similarity score based on shared lines
        output_lines = set(output.split('\n'))
        example_lines = set(example_report.split('\n'))
        similarity = len(output_lines.intersection(example_lines)) / len(example_lines)
        scores.append(similarity)

    top_index = scores.index(max(scores))
    print(f"Chosen output: {top_index + 1} (Score: {scores[top_index]:.4f})")
    return outputs[top_index], scores

def build_models():
    load_dotenv()

    mixtral_model: llm.Model = llm.get_model("groq-mixtral")
    gemma_model: llm.Model = llm.get_model("groq-gemma2")
    groq_llama3_1_405b_model: llm.Model = llm.get_model("groq-llama3.1-70b")

    return [mixtral_model, gemma_model, groq_llama3_1_405b_model]

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
    models = build_models()

    def prompt_model(model: Any, prompt: str) -> str:
        return model.prompt(prompt, system=POLICE_REPORT_SYSTEM_PROMPT).text()

    result = FusionChain.run(
        context={},
        models=models,
        callable=prompt_model,
        prompts=[user_prompt],
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
