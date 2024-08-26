import unittest
import os
import sys
import subprocess
import json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_prompts import generate_user_prompt, POLICE_REPORT_SYSTEM_PROMPT

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

    def test_prompt_with_ollama(self):
        user_prompt = generate_user_prompt(self.test_transcription, "General Occurrence")
        
        # Combine system and user prompts
        full_prompt = f"{POLICE_REPORT_SYSTEM_PROMPT}\n\n{user_prompt}"
        
        # Call Ollama CLI
        try:
            result = subprocess.run(
                ["ollama", "run", "llama3.1", full_prompt],
                capture_output=True,
                text=True,
                check=True
            )
            response = result.stdout

            # Check if the response exists
            self.assertTrue(response)
        except subprocess.CalledProcessError as e:
            self.fail(f"Ollama command failed: {e}")
        except FileNotFoundError:
            self.skipTest("Ollama is not installed or not in PATH")

if __name__ == '__main__':
    unittest.main()
