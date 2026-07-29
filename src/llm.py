import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

INPUT_PRICE = 0.10 / 1_000_000
OUTPUT_PRICE = 0.40 / 1_000_000


def llm(prompt):
    print("Using model:", "gemini-flash-latest")
    response = client.models.generate_content(
      model="gemini-3.1-flash-lite",
        contents=prompt
    )

    answer = response.text

    prompt_tokens = response.usage_metadata.prompt_token_count
    completion_tokens = response.usage_metadata.candidates_token_count
    total_tokens = response.usage_metadata.total_token_count

    cost = (
        prompt_tokens * INPUT_PRICE
        + completion_tokens * OUTPUT_PRICE
    )

    return {
        "answer": answer,
        "model": "gemini-3.1-flash-lite",
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "cost": cost
    }


if __name__ == "__main__":

    print(os.getenv("GEMINI_API_KEY"))

    result = llm("Hello")

    print(result)