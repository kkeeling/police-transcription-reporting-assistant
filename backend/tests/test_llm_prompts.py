import unittest
import os
from src.llm_prompts import generate_user_prompt, POLICE_REPORT_SYSTEM_PROMPT
import subprocess
import json

class TestLLMPrompts(unittest.TestCase):
    def setUp(self):
        # Load the test transcription from the file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_transcription_path = os.path.join(current_dir, 'test_transcription.txt')
        with open(test_transcription_path, 'r') as file:
            self.test_transcription = file.read().strip()

    def test_generate_user_prompt(self):
        prompt = generate_user_prompt(self.test_transcription)
        self.assertIn(self.test_transcription, prompt)
        self.assertIn("Incident Details", prompt)
        self.assertIn("Reporting Officer Information", prompt)

    def test_prompt_with_ollama(self):
        user_prompt = generate_user_prompt(self.test_transcription)
        
        # Combine system and user prompts
        full_prompt = f"{POLICE_REPORT_SYSTEM_PROMPT}\n\n{user_prompt}"
        
        # Call Ollama CLI
        try:
            result = subprocess.run(
                ["ollama", "run", "llama2", full_prompt],
                capture_output=True,
                text=True,
                check=True
            )
            response = result.stdout
            
            # Basic checks on the response
            self.assertIn("Incident Details", response)
            self.assertIn("July 15, 2023", response)
            self.assertIn("123 Oak Street", response)
            self.assertIn("noise complaint", response)
            
        except subprocess.CalledProcessError as e:
            self.fail(f"Ollama command failed: {e}")
        except FileNotFoundError:
            self.skipTest("Ollama is not installed or not in PATH")

if __name__ == '__main__':
    unittest.main()
