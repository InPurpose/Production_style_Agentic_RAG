# app.ingestion.indexer.py

from langchain_core.documents import Document

from rag_project.ingestion.chunker import *
from rag_project.ingestion.embedder import *
from rag_project.ingestion.vector_store import *

from rag_project.ingestion.document_loader import *

# from app.prepare_db.chunker import *
# from app.prepare_db.embedder import *
# from app.prepare_db.vector_store import *
# from app.ingestion.document_loader import *

class DocumentIndexer:

    def __init__(
        self,
        chunker:BaseChunker,
        embedder:BaseEmbedder,
        vector_store:BaseVectorStore,
    ):
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store


    def index_documents(self, documents:list[Document]):

        chunks = self.chunker.chunk(documents)

        vectors = self.embedder.embed_documents([c.text for c in chunks])

        self.vector_store.add_documents(chunks, vectors)


def main():
    from dotenv import load_dotenv
    load_dotenv() 
    
    if os.path.exists(PERSIST_DIRECTORY):
        shutil.rmtree(PERSIST_DIRECTORY)
    chunker = FixedSizeChunker()
    embedder = GeminiEmbedder()
    vector_store = ChromaVectorStore()

    index = DocumentIndexer(chunker,embedder,vector_store)

    document_loader = TextLoader()
    docs = document_loader.load()
    index.index_documents(docs)
if __name__ == '__main__':
    main()