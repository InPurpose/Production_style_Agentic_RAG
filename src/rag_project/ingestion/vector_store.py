# app.retrieval.vector_store.py

from langchain_core.documents import Document
# from langchain_chroma import Chroma
import chromadb

from rag_project.schemas import DocumentChunk
from rag_project.ingestion.embedder import *

class BaseVectorStore:

    def add_documents(self, chunks:list[DocumentChunk],vectors: list[list[float]]):
        raise NotImplementedError

    def similarity_search(self, embedded_query:list[list[float]], top_k: int = 5):
        raise NotImplementedError
    
    # def get_vector_store(self):
    #     raise NotImplementedError

PERSIST_DIRECTORY = "chroma_db"


class ChromaVectorStore(BaseVectorStore):

    def __init__(self, path:str= PERSIST_DIRECTORY,collection_name: str ='docs'):
        # print("Persist directory:", path)
        self.client = chromadb.PersistentClient(
            path=PERSIST_DIRECTORY
        )

        self.collection = self.client.get_or_create_collection(collection_name)

    def add_documents(self, chunks:list[DocumentChunk],vectors: list[list[float]]):
        # collection = self.client.get_or_create_collection("docs")
        self.collection.add(
            ids=[c.id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[c.metadata for c in chunks],
            embeddings=vectors
        )

        # print("Collection count:", self.collection.count())

    def similarity_search(self, embedded_query:list[float], top_k: int = 5):
        results = self.collection.query(
            query_embeddings=embedded_query,
            n_results=top_k,
            include=["documents", "metadatas","distances"],
        )

        return results
    
        for ids, documents, metadatas in zip(results["id"], results["text"], results["metadatas"]):
            for id, document, metadata in zip(ids, documents, metadatas):
                print(id, metadata)


    # def get_vector_store(self):
    #     return self.vector_store