from rag_project.ingestion.embedder import *
from rag_project.ingestion.vector_store import *

from rag_project.retrieval.retriever import Retriever
from rag_project.llm.llm_client import *

from rag_project.rag.prompt_builder import build_prompt


class RAGPipeline:
    
    def __init__(self, retriever:Retriever, llm:BaseLLM_Client,):

        self.retriever = retriever
        self.llm = llm

    def answer(self, query: str):
        results = self.retriever.retrieve(query)

        # print(type(chunks))
        # print(len(chunks))
        prompt = build_prompt(query, results)
        # print(prompt)

        response = self.llm.generate(prompt)

        sources = [
            {
                "id": chunk.id,
                "metadata": chunk.metadata
            }
            for chunk in results
            # for ids, metadatas in zip(chunks["ids"], chunks["metadatas"])
            # for id, metadata in zip(ids, metadatas)
        ]

        
        # print(sources)
        # print(prompt)
        answer = Answer(
            answer=response.text,
            sources=sources
        )
        # print(answer)
        return answer


def main():
    from dotenv import load_dotenv
    load_dotenv() 

    query = "What happens at the Mad Hatter's tea party?"

    embedder = GeminiEmbedder()
    vector_store = ChromaVectorStore()

    retriever = Retriever(embedder,vector_store)

    llm = GeminiLLM_Client()

    pipeline = RAGPipeline(retriever=retriever,llm=llm)

    answer = pipeline.answer(query)
    print(answer)

    # r.retrieve(query=query)

if __name__ == '__main__':
    main()