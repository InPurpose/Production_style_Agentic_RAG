# rag_project/retrieval/reranker.py
from rag_project.llm.llm_client import BaseLLM_Client
from langchain_core.prompts import ChatPromptTemplate

RERANKER_PROMPT = """
You are a relevance ranking model.

Given a query and a document chunk, rate how relevant the chunk is to the query.

Score from 1 to 10:
- 10 = highly relevant
- 1 = not relevant

ONLY output the number.

Query:
{query}

Chunk:
{chunk}
"""
# {chunk.text[:500]}

class BaseReranker:
    def rerank(self, query, chunks):
        raise NotImplementedError

class GeminiLLMReranker(BaseReranker):

    def __init__(self, llm:BaseLLM_Client):
        self.llm = llm

    def rerank(self, query, chunks):

        scored = []
        # i = 0
        for chunk in chunks:
            # print(f"DEBUG: current iteration{i}")
            # i+=1
            prompt_template = ChatPromptTemplate.from_template(RERANKER_PROMPT)
            prompt = prompt_template.format(query=query, chunk=chunk.text[:500])
            
            # prompt = RERANKER_PROMPT.format(query=query, chunk=chunk)

            response = self.llm.generate(prompt)

            try:
                score = float(response.text.strip())
            except (ValueError, Exception):
                score = 0

            scored.append((chunk, score))

        # sort（高分在前）
        scored.sort(key=lambda x: x[1], reverse=True)

        return [c for c, _ in scored]