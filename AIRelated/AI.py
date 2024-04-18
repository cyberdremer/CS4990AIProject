import getpass
import os

from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

_ = load_dotenv(find_dotenv())  # read local .env file


class AI:
    def __init__(self):
        os.environ["OPEN_API_KEY"] = getpass.getpass()
        self.llm_model = "gpt-3.5-turbo"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_completion(self, prompt):
        response = self.client.chat.completions.create(model=self.llm_model,
                                                       messages=prompt,
                                                       temperature=0.5,
                                                       max_tokens= 200)
        return response.choices[0].message.content



