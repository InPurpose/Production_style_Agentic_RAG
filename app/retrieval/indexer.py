class DocumentIndexer:

    def __init__(
        self,
        chunker,
        embedder,
        vector_store
    ):
        self.chunker = chunker
        self.embedder = embedder
        self.vector_store = vector_store


    def index_document(self, text: str, source: str):
        ...