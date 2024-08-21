import unittest
from transformers import pipeline
import torch
import os

class TestInsanelyFastWhisper(unittest.TestCase):
    def setUp(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3", device=device)

    def test_whisper_initialization(self):
        self.assertIsNotNone(self.pipe, "Whisper pipeline should be initialized")

    def test_whisper_transcription(self):
        # Use a real audio file for testing
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_audio_path = os.path.join(current_dir, "test_audio.wav")
        
        self.assertTrue(os.path.exists(test_audio_path), f"Test audio file not found: {test_audio_path}")
        
        result = self.pipe(test_audio_path)
        self.assertIsNotNone(result, "Transcription result should not be None")
        self.assertIn("text", result, "Transcription result should contain 'text' key")
        self.assertNotEqual(result["text"].strip(), "", "Transcription result should not be empty")

if __name__ == '__main__':
    unittest.main()
