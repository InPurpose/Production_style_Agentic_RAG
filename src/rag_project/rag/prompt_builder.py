from rag_project.schemas import DocumentChunk
from langchain_core.prompts import ChatPromptTemplate



PROMPT_TEMPLATE = """
Use ONLY the provided context.

If the answer is not contained in the context,
say "I don't know".

Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def build_prompt(question:str, chunks:list[DocumentChunk]):
    
    # _,document,metadata,_ = chunks[0]
    context_blocks = [
        f"[Context {i+1}] (Source: {chunk.source})\n{chunk.text}"
        for i ,chunk in enumerate(chunks)
    ]

    # for i ,() in enumerate(chunks):


    # for ids, documents, metadatas in zip(chunks["ids"], chunks["documents"], chunks["metadatas"]):
    #     for i,(id, document, metadata) in enumerate(zip(ids, documents, metadatas), start=0):
    #         context_blocks.append(
    #                 f"[Context {i+1}] (Source: {metadata['source']})\n{document}"
    #         )
        
    context = "\n\n".join(context_blocks)

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    prompt = prompt_template.format(context=context, question=question)

    return prompt