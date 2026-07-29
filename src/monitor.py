from src.db import get_connection


def log_conversation(
    question,
    answer,
    model,
    prompt_tokens,
    completion_tokens,
    total_tokens,
    cost
):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO conversations (
            question,
            answer,
            model,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            cost
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            question,
            answer,
            model,
            prompt_tokens,
            completion_tokens,
            total_tokens,
            cost
        )
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":

    log_conversation(
        question="Healthy breakfast",
        answer="Try oatmeal.",
        model="gemini-2.5-flash-lite",
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        cost=0.00003
    )

    print("Conversation logged successfully.")