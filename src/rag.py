from src.ingest import ingest
from src.llm import llm
from src.query_rewriter import rewrite_query
from src.reranker import rerank

df, index = ingest()

prompt_template = """
You are an expert AI Kitchen Assistant.

Your task is to answer the user's question using ONLY the recipes provided below.

Rules:
- Use only the information from the provided recipes.
- Do not make up ingredients, cooking steps, or nutrition facts.
- If the recipes do not contain enough information, reply:
  "I couldn't find enough information in the recipe database."
- Give a clear, concise, and well-structured answer.
- If multiple recipes match, briefly recommend the best options.

User Question:
{question}

Recipes:
{context}

Answer:
""".strip()

def build_prompt(query, search_results):

    context = ""

    for recipe in search_results:
        context += recipe["document"] + "\n\n"

    return prompt_template.format(
        question=query,
        context=context
    )


def rag(query):

    # Step 1: Rewrite user query
    rewritten_query = rewrite_query(query)

    # Step 2: Retrieve Top-10 documents
    search_results = index.search(
        query=rewritten_query,
        num_results=10
    )

    # Step 3: Re-rank retrieved documents
    search_results = rerank(
        rewritten_query,
        search_results
    )

    # Step 4: Keep best Top-5
    search_results = search_results[:5]

    # Step 5: Build prompt using original question
    prompt = build_prompt(
        query=query,
        search_results=search_results
    )

    # Step 6: Send prompt to LLM
    result = llm(prompt)

    return {
        "original_query": query,
        "rewritten_query": rewritten_query,
        "answer": result["answer"],
        "model": result["model"],
        "prompt_tokens": result["prompt_tokens"],
        "completion_tokens": result["completion_tokens"],
        "total_tokens": result["total_tokens"],
        "cost": result["cost"]
    }


if __name__ == "__main__":

    question = "I want a healthy breakfast"

    result = rag(question)

    print(result)