import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
        self.client = OpenAI(api_key=self.api_key)

    def generate_response(self, system_prompt: str, user_prompt: str, model: str = "gpt-4o", json_mode: bool = False) -> str:
        """
        Generates a response from the LLM.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        kwargs = {
            "model": model,
            "messages": messages,
        }
        
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}

        try:
            response = self.client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            if "insufficient_quota" in str(e):
                 raise Exception("OpenAI API Quota Exceeded. Please check your billing details at https://platform.openai.com/account/billing/overview.")
            raise e
