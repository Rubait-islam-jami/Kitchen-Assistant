def rerank(query, search_results):
    """
    Simple keyword-overlap reranker.
    """

    query_words = set(query.lower().split())

    scored = []

    for doc in search_results:

        text = (
            doc.get("title", "") + " " +
            doc.get("ingredients", "") + " " +
            doc.get("instructions", "")
        ).lower()

        score = sum(
            1 for word in query_words
            if word in text
        )

        scored.append((score, doc))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [doc for score, doc in scored]