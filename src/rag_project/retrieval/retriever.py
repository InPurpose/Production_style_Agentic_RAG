from rag_project.ingestion.embedder import BaseEmbedder, GeminiEmbedder
from rag_project.ingestion.vector_store import PERSIST_DIRECTORY, BaseVectorStore, ChromaVectorStore
from rag_project.schemas import RetrievedChunk
from rag_project.retrieval.reranker import BaseReranker, GeminiLLMReranker
from rag_project.retrieval.query_rewriter import QueryRewriter
from rag_project.retrieval.multi_query import MultiQueryGenerator


class Retriever:

    def __init__(self,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore,
        query_rewriter: QueryRewriter | None = None,
        multi_query: MultiQueryGenerator | None = None,
        reranker: BaseReranker | None = None
        ):

        self.embedder = embedder
        self.vector_store = vector_store
        self.query_rewriter = query_rewriter
        self.multi_query = multi_query
        self.reranker = reranker

    def retrieve(self, query: str, top_k: int = 5, history = None) -> list[RetrievedChunk]:
        
        # 1 rewrite
        if self.query_rewriter:
            query = self.query_rewriter.rewrite(query, history)
        
        queries = [query]
        
        # 2 multi-query
        if self.multi_query:
            generated = self.multi_query.generate(query)
            queries.extend(generated)
        
        all_results = []
        
        # 3 多次检索
        for q in queries:
            emb = self.embedder.embed_query(q)
            
            results = self.vector_store.similarity_search(
                embedded_query=emb,
                top_k=top_k * 2   # 多拿一点
            )
            
            parsed = [
                        RetrievedChunk(id=id, text=document, metadata=metadata, score=distance)
                        for ids, documents, distances, metadatas in zip(
                            results["ids"],
                            results["documents"],
                            results["distances"],
                            results["metadatas"]
                        )
                        for id, document, distance, metadata in zip(ids, documents, distances, metadatas)
                    ]
            all_results.extend(parsed)
        
        
        # 4 去重（非常关键）
        unique = {}
        for chunk in all_results:
            if chunk.id not in unique:
                unique[chunk.id] = chunk
            else:
                # 保留更高分（注意 distance 越小越好）
                if chunk.score < unique[chunk.id].score:
                    unique[chunk.id] = chunk
    
        results = list(unique.values())

        # 5 排序
        if self.reranker:
            results = self.reranker.rerank(query,results)
            print(f"Best score: {results[0].score}")
            print(f"Worst score: {results[top_k-1].score}")
            
            # results = self.reranker.rank(query, results)
        else:
            results.sort(key=lambda x: x.score)
        
        # return results
        return results[:top_k]
        
        
def main():
    from dotenv import load_dotenv
    load_dotenv() 
    
    query = """Explain the difference between S3 and EBS
            """
    embedder = GeminiEmbedder()
    vector_store = ChromaVectorStore()
    from rag_project.retrieval.multi_query import MultiQueryGenerator
    from rag_project.llm.llm_client import GeminiLLM_Client
    from rag_project.retrieval.query_rewriter import QueryRewriter
    
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
    
    results = r.retrieve(query=query, top_k=10)
    
    print("Queries:", query)
    
    print("Retrieved:", len(results))
    for result in results:
        print(result.text)
        print("="*50)
        
if __name__ == '__main__':
    main()