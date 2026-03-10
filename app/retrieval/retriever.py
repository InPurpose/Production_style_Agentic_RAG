class Retriever:

    def __init__(
        self,
        embedder,
        vector_store
    ):
        self.embedder = embedder
        self.vector_store = vector_store


    def retrieve(self, query: str, top_k: int = 5) -> list[DocumentChunk]:
        ...