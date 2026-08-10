import os
from google import genai
from config.settings import GOOGLE_API_KEY

class GeminiLLMClient:
    def __init__(self, model_name="gemini-2.5-flash"):
        self.client = genai.Client(api_key=GOOGLE_API_KEY)
        self.model_name = model_name

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={"system_instruction": system_instruction} if system_instruction else None
        )
        return response.text