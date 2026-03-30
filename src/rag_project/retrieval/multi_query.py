from rag_project.llm.llm_client import BaseLLM_Client, GeminiLLM_Client
from langchain_core.prompts import ChatPromptTemplate


MULTI_QUERY_PROMPT = """
Generate search queries for the question.

Rules:
- If the question involves multiple entities (e.g., A and B):
    1. Generate one query for A
    2. Generate one query for B
    3. Generate one query for the comparison
- Keep queries concise
- Output one query per line
- Do NOT number them

Question:
{query}

Queries:
"""

class MultiQueryGenerator:

    def __init__(self, llm:BaseLLM_Client, num_queries=3):
        self.llm = llm
        self.num_queries = num_queries

    def generate(self, query: str) -> list[str]:

        # prompt = MULTI_QUERY_PROMPT.format(num_queries=self.num_queries, query=query)
        prompt_template = ChatPromptTemplate.from_template(MULTI_QUERY_PROMPT)
        prompt = prompt_template.format(num_queries = self.num_queries,query=query)
        response = self.llm.generate(prompt)

        queries = response.text.strip().split("\n")

        # 清理空行
        queries = [q.strip() for q in queries if q.strip()]

        return queries
        
def main():
    llm = GeminiLLM_Client()
    generator = MultiQueryGenerator(llm)
    queries = generator.generate("")
    print(queries)

if __name__ == "__main__":
    main()