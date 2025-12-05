from google import genai
from dotenv import load_dotenv
import os


class Agent:
    def __init__(self):
        load_dotenv()
        api = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=api)
        

    def ask(self, question):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
        )
        return response.text
    
    