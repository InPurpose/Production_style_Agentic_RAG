# tests/test_embedder.py
from dotenv import load_dotenv
load_dotenv()
import time
from rag_project.ingestion.embedder import GeminiEmbedder


class FakeModel:
    def __init__(self):
        self.calls = 0

    def embed_documents(self, texts):
        self.calls += 1
        return [[0.1] * 10 for _ in texts]

def test_batch_calls():

    fake_model = FakeModel()
    embedder = GeminiEmbedder(model=fake_model)

    texts = [str(i) for i in range(1000)]

    embedder.embed_documents(texts)

    print("API calls:", fake_model.calls)

    assert fake_model.calls < 50  # 应该是 batch 次数