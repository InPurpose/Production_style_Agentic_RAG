from fastapi import FastAPI
# from rag_project.rag.pipeline import RAGPipeline

app = FastAPI()

pipeline = RAGPipeline()


@app.post("/query")
def query(q: str):
    return pipeline.query(q)