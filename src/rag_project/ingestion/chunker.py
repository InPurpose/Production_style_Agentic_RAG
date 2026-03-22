# app.retrieval.chunker.py

# from dataclasses import dataclass
import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag_project.schemas import DocumentChunk


def generate_chunk_id(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class BaseChunker:
    def chunk(self, docs: list[Document]) -> list:
        raise NotImplementedError


class FixedSizeChunker(BaseChunker):
    def __init__(self, chunk_size: int = 800, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.overlap,
            length_function=len,
            separators=["\n\n", "\n", ".", "!", "?"],
            add_start_index=True,
        )

    def chunk(self, docs: list[Document]) -> list[DocumentChunk]:
        docs = [d for d in docs if d is not None]
        chunks = self.text_splitter.split_documents(docs)

        results = []

        # if len(chunks) >0:
        #     print(chunks[0].metadata.keys)
        for i, chunk in enumerate(chunks):
            metadata = chunk.metadata
            id = generate_chunk_id(chunk.page_content)
            chunk = DocumentChunk(id=id, text=chunk.page_content, metadata=metadata)

            results.append(chunk)

        return results


def main(): ...


if __name__ == "__main__":
    main()
