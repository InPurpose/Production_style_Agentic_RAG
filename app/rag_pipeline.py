class RAGPipeline:

    def __init__(
        self,
        retriever,
        llm
    ):
        self.retriever = retriever
        self.llm = llm


    def answer(self, query: str):
        ...