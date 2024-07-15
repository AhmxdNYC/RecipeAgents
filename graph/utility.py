import os
from typing import List
from langchain_core.pydantic_v1 import BaseModel
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
# Enforces Model Output to be a List of Strings

class Queries(BaseModel):
    queries: List[str]
    
model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

tavily = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])