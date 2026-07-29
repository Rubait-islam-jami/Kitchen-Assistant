from flask import Flask, request

from src.rag import rag
from src.monitor import log_conversation
from src.evaluate import log_evaluation

app = Flask(__name__)


@app.get("/")
def home():

    return {
        "message": "Kitchen Assistant API is running!"
    }


@app.post("/ask")
def ask():

    data = request.get_json()

    question = data["question"]

    result = rag(question)

    answer = result["answer"]

    log_conversation(
        question=question,
        answer=answer,
        model=result["model"],
        prompt_tokens=result["prompt_tokens"],
        completion_tokens=result["completion_tokens"],
        total_tokens=result["total_tokens"],
        cost=result["cost"]
    )

    return {
        "question": question,
        "answer": answer,
        "usage": {
            "model": result["model"],
            "prompt_tokens": result["prompt_tokens"],
            "completion_tokens": result["completion_tokens"],
            "total_tokens": result["total_tokens"],
            "cost": result["cost"]
        }
    }


@app.post("/evaluate")
def evaluate():

    data = request.get_json()

    question = data["question"]
    answer = data["answer"]
    relevance = data["relevance"]

    log_evaluation(
        question=question,
        answer=answer,
        relevance=relevance
    )

    return {
        "status": "Evaluation logged successfully."
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )