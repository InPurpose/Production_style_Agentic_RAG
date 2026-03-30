from rag_project.retrieval.retriever import Retriever
from rag_project.llm.llm_client import BaseLLM_Client
class AgentExecutor:

    def __init__(self, retriever: Retriever, llm: BaseLLM_Client):
        self.retriever = retriever
        self.llm = llm

    def run(self, query, plan):

        context = []
        answer = None
        
        for step in plan:

            if step["action"] == "retrieve":
                results = self.retriever.retrieve(step["query"])
                context.extend(results)
        
            elif step["action"] == "final":
                answer = self.llm.generate(context + query)

        return answer
        
    def _final_answer(self, query, context):
    
        context_text = "\n\n".join(context[:10])  # 控制长度

        prompt = f"""
                Answer the question using the context below.
                
                Context:
                {context_text}
                
                Question:
                {query}
                
                Answer:
                """

        response = self.llm.generate(prompt)

        return response.text
        
        

def main():
    from dotenv import load_dotenv
    load_dotenv() 
    
    from rag_project.ingestion.embedder import GeminiEmbedder
    from rag_project.ingestion.vector_store import ChromaVectorStore

    query = """Explain the difference between S3 and EBS
            """
    embedder = GeminiEmbedder()
    vector_store = ChromaVectorStore()
    from rag_project.retrieval.multi_query import MultiQueryGenerator
    from rag_project.llm.llm_client import GeminiLLM_Client
    from rag_project.retrieval.query_rewriter import QueryRewriter
    from rag_project.retrieval.reranker import GeminiLLMReranker
    from rag_project.retrieval.retriever import Retriever

    llm = GeminiLLM_Client()
    
    query_rewriter = QueryRewriter(llm)
    rewritten = query_rewriter.rewrite(query)
    print("Rewritten query:", rewritten)
    
    multi_query = MultiQueryGenerator(llm)
    print("Multi queries:", multi_query.generate(rewritten))
    
    reranker = GeminiLLMReranker(llm)
    # return
 
    r = Retriever(
                embedder = embedder,
                vector_store = vector_store,
                query_rewriter=query_rewriter,
                multi_query=multi_query, 
                reranker=reranker,
                )
    
    results = r.retrieve(query=query, top_k=5)
    
    print("Queries:", query)
    
    print("Retrieved:", len(results))
    for result in results:
        print(result.text)
        print("="*50)
        
if __name__ == '__main__':
    main()