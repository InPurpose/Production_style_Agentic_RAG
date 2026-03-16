# src/rag_project/schema/query.py

from pydantic import BaseModel

class Query(BaseModel):

    question: str
    top_k: int = 5