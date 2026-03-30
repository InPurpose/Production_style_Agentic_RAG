from langchain_core.prompts import ChatPromptTemplate
from rag_project.llm.llm_client import GeminiLLM_Client
import json

PLANNER_PROMPT = """
You are an AI planner.

Break the user question into a sequence of steps.

Each step must be one of:
- retrieve: to get information
- final: to produce the final answer

Rules:
- If the question involves multiple entities, create separate retrieve steps
- Keep each step simple
- Output ONLY valid JSON (a list of steps)
- The "final" step should NOT include a query

Question:
{query}

Output format:
[
  {{"action": "retrieve", "query": "..."}},
  ...
]
"""

class Planner:

    def __init__(self, llm):
        self.llm = llm

    def plan(self, query:str):
        
        prompt_template = ChatPromptTemplate.from_template(PLANNER_PROMPT)
        prompt = prompt_template.format(query=query)
        
        response = self.llm.generate(prompt)

        try:
            plan = json.loads(response.text)
        except Exception:
            # fallback（很重要）
            plan = [
                {"action": "retrieve", "query": query},
                {"action": "final"}
            ]

        return plan
        
def main():
    from dotenv import load_dotenv
    load_dotenv()
    
    llm = GeminiLLM_Client()
    planner = Planner(llm)
    
    plan = planner.plan("Explain the difference between S3 and EBS")
    
    print(plan)

if __name__ == "__main__":
    main()
