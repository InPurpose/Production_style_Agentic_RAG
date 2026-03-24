# app.retrieval.embedder.py


import random
import time

import os
# import shutil
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
from rag_project.schemas import DocumentChunk


# DATABASE_PATH = "chroma_db"

class BaseEmbedder:

    def embed_documents(self, texts: list[DocumentChunk]) -> list[list[float]]:
        raise NotImplementedError

    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError
    

class GeminiEmbedder(BaseEmbedder):
    def __init__(self,model = None):

        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(" Please provide GEMINI_API_KEY as an environment variable")
        if not model:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            self.model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001"
            )
        else:
            self.model = model
            
    def embed_query(self, query: str) -> list[float]:
        return self.model.embed_query(query)

    def embed_documents(self, texts: list[DocumentChunk]) -> list[list[float]]:

        batch_size = 100   # 🔥 关键参数
        results = []

        for i in range(0,len(texts), batch_size):

            batch = texts[i:i+batch_size]

            vectors = self.embed_with_retry(batch)

            results.extend(vectors)
            if i%100 == 0:
                print(f"Batched {(i+1)}/{len(texts)}")

            # 🔥 避免打爆 API
            # time.sleep(1)


        return results
        # return self.model.embed_documents(texts)

  

    def embed_with_retry(self, texts, max_retries=5):
        
        for attempt in range(max_retries):
            try:
                return self.model.embed_documents(texts)
            
            except Exception as e:
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    print(f"Rate limited. Retry in {wait:.2f}s")
                    time.sleep(wait)
                else:
                    raise e

        raise Exception("Max retries exceeded")


    