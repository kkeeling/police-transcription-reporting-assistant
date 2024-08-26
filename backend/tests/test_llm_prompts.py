import unittest
import os
import sys
from unittest.mock import patch

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_prompts import generate_user_prompt, generate_report, POLICE_REPORT_SYSTEM_PROMPT
from src.ollama_client import OllamaClient

class TestLLMPrompts(unittest.TestCase):
    def setUp(self):
        # Load the test transcription from the file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_transcription_path = os.path.join(current_dir, 'test_transcription.txt')
        with open(test_transcription_path, 'r') as file:
            self.test_transcription = file.read().strip()

    def test_generate_user_prompt_general_occurrence(self):
        prompt = generate_user_prompt(self.test_transcription, "General Occurrence")
        self.assertIn(self.test_transcription, prompt)
        self.assertIn("General Occurrence", prompt)

    def test_generate_user_prompt_crown_brief(self):
        prompt = generate_user_prompt(self.test_transcription, "Crown Brief")
        self.assertIn(self.test_transcription, prompt)
        self.assertIn("Crown Brief", prompt)

    def test_generate_user_prompt_invalid_type(self):
        with self.assertRaises(ValueError):
            generate_user_prompt(self.test_transcription, "Invalid Type")

    @patch.object(OllamaClient, 'run_ollama_model')
    def test_generate_report(self, mock_run_ollama_model):
        mock_run_ollama_model.return_value = "This is a mock police report."
        
        report = generate_report(self.test_transcription, "General Occurrence", "llama3")
        
        self.assertEqual(report, "This is a mock police report.")
        mock_run_ollama_model.assert_called_once()
        
        # Check that the prompt passed to run_ollama_model contains the necessary components
        call_args = mock_run_ollama_model.call_args[0]
        self.assertEqual(call_args[0], "llama3")
        self.assertIn(POLICE_REPORT_SYSTEM_PROMPT, call_args[1])
        self.assertIn(self.test_transcription, call_args[1])
        self.assertIn("General Occurrence", call_args[1])

if __name__ == '__main__':
    unittest.main()
