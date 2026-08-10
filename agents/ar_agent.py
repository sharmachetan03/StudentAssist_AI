import logging
import os
from google import genai
from google.genai import types
from schema.models import UserQueryRequest

logger = logging.getLogger(__name__)


class ARAgent:

    def __init__(self):
        # Initializes client using GEMINI_API_KEY from environment variables
        self.client = genai.Client()
        self.model_name = "gemini-3.6-flash"

    def build_prompt(self, request: UserQueryRequest) -> str:
        """Constructs a structured prompt for the Gemini API safely handling flat schema fields."""
        category = getattr(request, "category", "General Academic Query")

        return f"""
        You are an intelligent Academic Assistant AI.
        
        Student Context:
        - Student ID: {request.student_id}
        - Category/Topic: {category}
        
        Student Query:
        "{request.query}"
        
        Provide a concise, helpful, and clear answer for the student.
        """

    def generate_response(self, request: UserQueryRequest) -> str:
        """Sends the request to Gemini and returns the generated academic response."""
        try:
            logger.info(
                f"ARAgent: Generating response for Student ID {request.student_id}..."
            )

            prompt = self.build_prompt(request)

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,
                ),
            )

            return response.text

        except Exception as e:
            logger.error(f"ARAgent failed to generate response: {str(e)}")
            raise e