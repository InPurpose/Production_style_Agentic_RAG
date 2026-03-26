# apps/streamlit_app.py
from dotenv import load_dotenv

load_dotenv()

import streamlit as st


from rag_project.ingestion.embedder import *
from rag_project.ingestion.vector_store import *
from rag_project.retrieval.retriever import Retriever
from rag_project.llm.llm_client import *
from rag_project.rag.pipeline import RAGPipeline


embedder = GeminiEmbedder()
vector_store = ChromaVectorStore()

retriever = Retriever(embedder,vector_store)

llm = GeminiLLM_Client()

pipeline = RAGPipeline(retriever=retriever,llm=llm)

st.title("RAG Demo")

query = st.text_input("Ask a question")

if query:
    answer_obj = pipeline.answer(query)
    
    # 显示答案（支持Markdown渲染）
    st.markdown("### Answer")
    st.markdown(answer_obj.answer)
    
    # 显示来源
    if answer_obj.sources:
        st.markdown("### Sources")
        for i, source in enumerate(answer_obj.sources, 1):
            source_id = source.get('id', 'unknown')
            metadata = source.get('metadata', {})
            start_index = metadata.get('start_index', 'unknown')
            source_name = metadata.get('source', 'unknown')
            
            with st.expander(f"source {i}: {source_id} (index: {start_index})"):
                st.write(f"**document:** {source_name}")
                st.json(source)  # 完整显示，或自定义