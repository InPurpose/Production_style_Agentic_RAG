# src/rag_project/main.py
from dotenv import load_dotenv
load_dotenv() 

from rag_project.ingestion.embedder import *
from rag_project.ingestion.vector_store import *
from rag_project.retrieval.retriever import Retriever
from rag_project.llm.llm_client import *
from rag_project.rag.pipeline import RAGPipeline

import argparse

parser = argparse.ArgumentParser(description="RAG Project Main")
parser.add_argument('query', help="must search with query, example: 'what is RAG?'")

args = parser.parse_args()

query = args.query
# query = "What happens at the Mad Hatter's tea party?"

embedder = GeminiEmbedder()
vector_store = ChromaVectorStore()

retriever = Retriever(embedder,vector_store)

llm = GeminiLLM_Client()

pipeline = RAGPipeline(retriever=retriever,llm=llm)

answer = pipeline.answer(query)
print(answer)

