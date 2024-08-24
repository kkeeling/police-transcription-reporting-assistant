import unittest
from src.llm_prompts import generate_user_prompt, POLICE_REPORT_SYSTEM_PROMPT
import subprocess
import json

class TestLLMPrompts(unittest.TestCase):
    def test_generate_user_prompt(self):
        transcription = "At approximately 10:30 PM, I observed a red vehicle speeding on Main Street."
        prompt = generate_user_prompt(transcription)
        self.assertIn(transcription, prompt)
        self.assertIn("Incident Details", prompt)
        self.assertIn("Reporting Officer Information", prompt)

    def test_prompt_with_ollama(self):
        transcription = "At 9:45 PM on July 15, 2023, I responded to a noise complaint at 123 Oak Street."
        user_prompt = generate_user_prompt(transcription)
        
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
