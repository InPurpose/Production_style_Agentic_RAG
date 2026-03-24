from dotenv import load_dotenv

load_dotenv()

import os
import shutil

from rag_project.ingestion.chunker import *
from rag_project.ingestion.document_loader import *
from rag_project.ingestion.embedder import *
from rag_project.ingestion.indexer import DocumentIndexer
from rag_project.ingestion.vector_store import *

if os.path.exists(PERSIST_DIRECTORY):
    shutil.rmtree(PERSIST_DIRECTORY)

chunker = FixedSizeChunker()
embedder = GeminiEmbedder()
vector_store = ChromaVectorStore()

index = DocumentIndexer(chunker, embedder, vector_store)



# txt_loader = TextFileLoader("data/")
# txt_file = txt_loader.load()

# pdf_loader = PDFLoader("data/")
# pdf_file = pdf_loader.load()

# index.index_documents(txt_file)
# index.index_documents(pdf_file)

loader = UnifiedLoader()
documents = loader.load()
index.index_documents(documents)
