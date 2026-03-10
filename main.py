from fastapi import FastAPI

app = FastAPI()

rag_pipeline = ...


@app.post("/ask")
def ask_question(query: str):
    answer = rag_pipeline.answer(query)
    return {"answer": answer}