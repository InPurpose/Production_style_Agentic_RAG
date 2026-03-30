from langchain_core.prompts import ChatPromptTemplate
from rag_project.llm.llm_client import BaseLLM_Client, GeminiLLM_Client

QUERY_REWRITER_PROMPT = """
You are an expert in search query optimization.

Your task is to rewrite the user's question into a clear, standalone query
that is optimized for document retrieval.

Requirements:
- Resolve pronouns (e.g., "it", "its", "they")
- Replace vague references with explicit terms
- Include important keywords
- Keep it concise
- DO NOT combine multiple questions into one sentence
- DO NOT add explanations
- Output ONLY ONE query

Conversation history:
{history_text}

User question:
{query}

Rewritten query:
"""
class QueryRewriter:

    def __init__(self, llm: BaseLLM_Client):
        self.llm = llm

    def rewrite(self, query: str, history=None) -> str:

        if history:
            history_text = "\n".join(
                [f"User: {h[0]}\nAssistant: {h[1]}" for h in history]
            )
        else:
            history_text = ""
            
        prompt_template = ChatPromptTemplate.from_template(QUERY_REWRITER_PROMPT)
        prompt = prompt_template.format(history_text=history_text, query=query)

        response = self.llm.generate(prompt)

        return response.text.strip()
        
def main():
    from dotenv import load_dotenv
    load_dotenv() 
    query = """
    User: What is BM25?
    User: How is it different from vector search?
    User: Which one should I use?
    """
    print(f"Original query: {query}")
    rewriter = QueryRewriter(GeminiLLM_Client())
    rewritten_query = rewriter.rewrite(query=query)
    print(f"Rewritten query: {rewritten_query}")
    

if __name__ == '__main__':
    main()