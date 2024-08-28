import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_prompts import generate_user_prompt, generate_report, POLICE_REPORT_SYSTEM_PROMPT

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

    @patch('llm.get_model')
    @patch('src.llm_prompts.FusionChain.run')
    def test_generate_report(self, mock_fusion_chain_run, mock_get_model):
        mock_model = MagicMock()
        mock_get_model.side_effect = [mock_model, mock_model, mock_model]
        
        mock_fusion_chain_result = MagicMock()
        mock_fusion_chain_result.top_response = "This is a mock police report."
        mock_fusion_chain_run.return_value = mock_fusion_chain_result

        report = generate_report(self.test_transcription, "General Occurrence")
        
        self.assertEqual(report, "This is a mock police report.")
        mock_get_model.assert_any_call("gemma2")
        mock_get_model.assert_any_call("llama3.1")
        mock_get_model.assert_any_call("mistral")
        mock_fusion_chain_run.assert_called_once()
        
        # Check that the FusionChain.run method was called with the correct arguments
        call_args = mock_fusion_chain_run.call_args[1]
        self.assertIn('context', call_args)
        self.assertIn('models', call_args)
        self.assertIn('callable', call_args)
        self.assertIn('prompts', call_args)
        self.assertIn('evaluator', call_args)
        self.assertIn('get_model_name', call_args)
        
        # Check that the prompt contains the necessary components
        user_prompt = call_args['prompts'][0]
        self.assertIn(self.test_transcription, user_prompt)
        self.assertIn("General Occurrence", user_prompt)

if __name__ == '__main__':
    unittest.main()
