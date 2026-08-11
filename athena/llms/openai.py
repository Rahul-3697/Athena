import os

from dotenv import load_dotenv
from openai import OpenAI

from athena.llms.base import BaseLLM

load_dotenv()


class OpenAILLM(BaseLLM):

    def __init__(self, model: str = "gpt-4"):
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.model = model

    def invoke(self, prompt: str) -> str:

        response = self.client.responses.create(
            model=self.model,
            input=prompt
        )

        return response.output_text