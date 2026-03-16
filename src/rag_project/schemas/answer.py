# src/rag_project/schema/answer.py

from pydantic import BaseModel

class Answer(BaseModel):

    answer: str
    sources: list[dict]

    def __str__(self):

        source_text = "\n".join(f"- {s}" for s in self.sources)

        return f"""
Answer
------
{self.answer}

Sources
-------
{source_text}
"""