import os
from langchain_google_genai import ChatGoogleGenerativeAI
from rag_project.schemas import Answer


class BaseLLM_Client():
    def generate(self,prompt:str):
        raise NotImplementedError
    

class GeminiLLM_Client(BaseLLM_Client):
    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(" Please provide GEMINI_API_KEY as an environment variable")
        
        self.model = ChatGoogleGenerativeAI(model="gemini-3-pro-preview")


    def generate(self,prompt:str):
        response = self.model.invoke(prompt)
        response_text = response.text
        
        # print(response_text)
        
        return response
    

