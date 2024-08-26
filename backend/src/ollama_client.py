import subprocess
import json

class OllamaClient:
    def __init__(self):
        self.base_command = ["ollama"]

    def run_ollama_model(self, model_name, prompt):
        command = self.base_command + ["run", model_name, prompt]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running Ollama model: {e}")
            return None

    def list_models(self):
        command = self.base_command + ["list"]
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:]]
            return models
        except subprocess.CalledProcessError as e:
            print(f"Error listing Ollama models: {e}")
            return []

    def switch_model(self, model_name):
        # In Ollama, switching models is just a matter of using a different model name
        # We'll just check if the model exists
        if model_name in self.list_models():
            return True
        else:
            print(f"Model {model_name} not found")
            return False
