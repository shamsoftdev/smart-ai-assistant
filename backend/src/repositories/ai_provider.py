import os
from google import genai


class AIProvider:

    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def generate(self, prompt: str):
        response =  self.client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config={
                "temperature": 0.2
            }
        )
        return response.text if hasattr(response, "text") else str(response)