# app.retrieval.embedder.py

import os
import shutil
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from rag_project.schemas import DocumentChunk


# DATABASE_PATH = "chroma_db"

class BaseEmbedder:

    def embed_documents(self, texts: list[DocumentChunk]) -> list[list[float]]:
        raise NotImplementedError

    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError
    

class GeminiEmbedder(BaseEmbedder):
    def __init__(self):

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(" Please provide GEMINI_API_KEY as an environment variable")
        
        self.model = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
        )
            
    def embed_query(self, query: str) -> list[float]:
        return self.model.embed_query(query)

    def embed_documents(self, texts: list[DocumentChunk]) -> list[list[float]]:
        return self.model.embed_documents(texts)







    
    