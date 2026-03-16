# src/rag_project/schema/retrieved_chunk.py

from pydantic import BaseModel
from typing import Dict


class RetrievedChunk(BaseModel):

    id: str
    text: str
    metadata: Dict
    score: float

    @property
    def source(self):
        return self.metadata.get("source")