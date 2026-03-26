
# from langchain_core.documents import Document
# from langchain_chroma import Chroma
import chromadb
import os

from rag_project.schemas import DocumentChunk
# from rag_project.ingestion.embedder import *

class BaseVectorStore:

    def add_documents(self, chunks:list[DocumentChunk],vectors: list[list[float]]):
        raise NotImplementedError

    def similarity_search(self, embedded_query:list[float], top_k: int = 5):
        raise NotImplementedError
    
    # def get_vector_store(self):
    #     raise NotImplementedError

PERSIST_DIRECTORY = os.getenv("CHROMA_PATH", "chroma_db")


class ChromaVectorStore(BaseVectorStore):

    def __init__(self, path:str= PERSIST_DIRECTORY,collection_name: str ='docs'):
        # print("Persist directory:", path)
        self.client = chromadb.PersistentClient(
            path=PERSIST_DIRECTORY
        )

        self.collection = self.client.get_or_create_collection(collection_name)

    def add_documents(self, chunks:list[DocumentChunk],vectors: list[list[float]]):
        print(f"Original chunks: {len(chunks)}")

        existing_ids = set(self.collection.get()["ids"])
        seen_ids = set()

        new_chunks = []
        new_vectors = []

        for chunk, vector in zip(chunks, vectors):

            # 🔥 1. 跳过 DB 已存在           🔥 2. 跳过当前 batch 重复
            if chunk.id in existing_ids or chunk.id in seen_ids:
                continue

            seen_ids.add(chunk.id)
            new_chunks.append(chunk)
            new_vectors.append(vector)

        print(f"After dedupe: {len(new_chunks)}")

        if not new_chunks:
            print("No new chunks to add.")
            return
        
        total = len(new_chunks)
        print(f"Adding {total} chunks to vector store...")
        batch_size = 5000
        for i in range(0, total, batch_size):
        
            batch_chunks = new_chunks[i:i+batch_size]
            batch_vectors = new_vectors[i:i+batch_size]
    
            print(f"Adding batch {i//batch_size + 1} ({len(batch_chunks)})")
    
            self.collection.add(
                ids=[c.id for c in batch_chunks],
                documents=[c.text for c in batch_chunks],
                metadatas=[c.metadata for c in batch_chunks],
                embeddings=batch_vectors
            )
        
        
        # self.collection.add(
        #     ids=[c.id for c in new_chunks],
        #     documents=[c.text for c in new_chunks],
        #     metadatas=[c.metadata for c in new_chunks],
        #     embeddings=new_vectors
        # )
        

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