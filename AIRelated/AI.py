import getpass
import json
import os

import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

from langchain.document_loaders.json_loader import JSONLoader
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

_ = load_dotenv(find_dotenv())  # read local .env file


class AI:
    def __init__(self):
        self.llm_model = "gpt-3.5-turbo"
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def get_completion(self, prompt):
        response = self.client.chat.completions.create(model=self.llm_model,
                                                       messages=prompt,
                                                       temperature=0.0,
                                                       max_tokens=200)
        return response.choices[0].message.content
