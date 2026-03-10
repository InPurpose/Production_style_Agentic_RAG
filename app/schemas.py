# app/schemas.py

from dataclasses import dataclass
from typing import Dict


@dataclass
class DocumentChunk:
    content: str
    source: str
    chunk_id: int
    metadata: Dict