from rag_project.ingestion.embedder import *
from rag_project.ingestion.vector_store import *
from rag_project.schemas import RetrievedChunk


class Retriever:

    def __init__(self,embedder: BaseEmbedder,vector_store:BaseVectorStore):

        self.embedder = embedder
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        embedded_query = self.embedder.embed_query(query)
        search_results = self.vector_store.similarity_search(
            embedded_query=embedded_query,
            top_k=top_k
            )
        
        # print(search_results["included"])
        # for metadata in search_results["metadatas"]:
        #     print(metadata)

        # for ids, distances, metadatas in zip(search_results["ids"], search_results["distances"], search_results["metadatas"]):
        #     for id, distance, metadata in zip(ids, distances, metadatas):
        #         print(f"{id} : {metadata} | distance: {distance}")
        res: list[RetrievedChunk] = [
            RetrievedChunk(id=id,text=document,metadata=metadata,score=distance)
            for ids,documents,distances, metadatas in zip(search_results["ids"], search_results["documents"],search_results["distances"], search_results["metadatas"])
            for id, document,distance, metadata in zip(ids, documents,distances, metadatas)
        ]
        # return search_results
        return res


def main():
    from dotenv import load_dotenv
    load_dotenv() 
    query = "What happens at the Mad Hatter's tea party?"
    embedder = GeminiEmbedder()
    vector_store = ChromaVectorStore()
    r = Retriever(embedder,vector_store)
    r.retrieve(query=query)

if __name__ == '__main__':
    main()