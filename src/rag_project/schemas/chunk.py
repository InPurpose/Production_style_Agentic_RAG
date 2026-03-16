# src/rag_project/schema/chunk.py

from dataclasses import dataclass
from typing import Dict, Optional
from pydantic import BaseModel



class DocumentChunk(BaseModel):
    
    id: str
    text: str

    metadata: Dict = {}

    # metadata{
    #     source: str
    #     page: Optional[int] = None
    #     chunk_index: int
    #     embedding: Optional[list[float]] = None
    # }
