"""
This module contains system and user prompts for LLMs used in police report generation.
"""

# System prompt for police report generation
POLICE_REPORT_SYSTEM_PROMPT = """
You are an AI assistant trained to generate police reports based on audio transcriptions.
Your task is to create clear, concise, and accurate reports that follow standard police report formats.
Focus on presenting factual information without bias or interpretation.
Include all relevant details from the transcription, organizing them in a logical and chronological order.
Use professional language and avoid colloquialisms or slang.
"""

# Template for user prompt with placeholders for transcription data
POLICE_REPORT_USER_PROMPT_TEMPLATE = """
Based on the following audio transcription, generate a police report:

Transcription:
{transcription}

Please include the following sections in your report:
1. Incident Details (Date, Time, Location)
2. Reporting Officer Information
3. Incident Summary
4. Witness Statements (if any)
5. Evidence Collected (if any)
6. Actions Taken
7. Follow-up Required (if any)

Ensure that the report is factual, objective, and follows standard police report formatting.
"""

def generate_user_prompt(transcription: str) -> str:
    """
    Generate a user prompt for police report generation based on the given transcription.

    Args:
        transcription (str): The transcribed audio content.

    Returns:
        str: The formatted user prompt with the transcription inserted.
    """
    return POLICE_REPORT_USER_PROMPT_TEMPLATE.format(transcription=transcription)
