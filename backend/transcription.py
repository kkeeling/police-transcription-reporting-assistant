import torch
from transformers import pipeline
from transformers.utils import is_flash_attn_2_available

def transcribe_audio(file_path, device="cuda:0", model_name="openai/whisper-large-v3", batch_size=24, chunk_length_s=30):
    """
    Transcribe audio using Insanely Fast Whisper.

    Args:
    file_path (str): Path to the audio file.
    device (str): Device to use for inference. Default is "cuda:0".
    model_name (str): Name of the Whisper model to use. Default is "openai/whisper-large-v3".
    batch_size (int): Batch size for processing. Default is 24.
    chunk_length_s (int): Length of audio chunks in seconds. Default is 30.

    Returns:
    dict: Transcription output including text and timestamps.
    """
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model_name,
        torch_dtype=torch.float16,
        device=device,
        model_kwargs={"attn_implementation": "flash_attention_2"} if is_flash_attn_2_available() else {"attn_implementation": "sdpa"},
    )

    outputs = pipe(
        file_path,
        chunk_length_s=chunk_length_s,
        batch_size=batch_size,
        return_timestamps=True,
    )

    return outputs

def handle_transcription(file_path):
    """
    Handle the transcription process and return the result.

    Args:
    file_path (str): Path to the audio file.

    Returns:
    dict: Transcription output.
    """
    try:
        result = transcribe_audio(file_path)
        return {"success": True, "transcription": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
