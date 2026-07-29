from src.db import get_connection


def log_evaluation(question, answer, relevance):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO evaluations (
            question,
            answer,
            relevance
        )
        VALUES (?, ?, ?)
        """,
        (
            question,
            answer,
            relevance
        )
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":

    log_evaluation(
        question="Healthy breakfast",
        answer="Try oatmeal with fruits.",
        relevance=5
    )

    print("Evaluation logged successfully.")