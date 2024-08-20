import unittest
from transformers import pipeline
from optimum.bettertransformer import BetterTransformer

class TestInsanelyFastWhisper(unittest.TestCase):
    def setUp(self):
        self.pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
        self.pipe.model = BetterTransformer.transform(self.pipe.model)

    def test_whisper_initialization(self):
        self.assertIsNotNone(self.pipe, "Whisper pipeline should be initialized")

    def test_whisper_transcription(self):
        # This is a basic test. In a real scenario, you'd use a short audio file.
        test_text = "Hello, this is a test."
        result = self.pipe(test_text)
        self.assertIsNotNone(result, "Transcription result should not be None")
        self.assertIn("text", result, "Transcription result should contain 'text' key")

if __name__ == '__main__':
    unittest.main()
