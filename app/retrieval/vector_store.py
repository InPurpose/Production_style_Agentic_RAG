from langchain_core.documents import Document
from langchain_chroma import Chroma

class BaseVectorStore:

    def add_documents(self, docs, embeddings):
        raise NotImplementedError

    def similarity_search(self, query_embedding, top_k: int = 5):
        raise NotImplementedError
    

class ChromaVectorStore(BaseVectorStore):

    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    def add_documents(docs: list[Document]):
        ...
    def similarity_search(query:str):
        ...