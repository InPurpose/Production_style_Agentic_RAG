class BaseEmbedder:

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_query(self, query: str) -> list[float]:
        raise NotImplementedError
    

class GeminiEmbedder(BaseEmbedder):
    ...