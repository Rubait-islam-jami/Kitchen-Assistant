import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-3.1-flash-lite"


def rewrite_query(query):

    prompt = f"""
You are an expert cooking assistant.

Rewrite the user's question so it is clearer and easier for a recipe retrieval system to search.

Rules:
- Keep the same meaning.
- Do not answer the question.
- Return only the rewritten query.

Question:
{query}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    return response.text.strip()