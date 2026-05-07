from app.db import collection


def get_documents():

    docs = collection.find({})

    documents = []

    for d in docs:

        objectives = d.get("objectives", [])

        text = f"""
        {d.get("title", "")}
        {d.get("introduction", "")}
        {d.get("actionPlan", "")}
        {d.get("expectedOutcome", "")}
        {' '.join(map(str, objectives))}
        """

        documents.append({
            "id": str(d.get("_id")),
            "title": d.get("title", ""),
            "text": text.strip()
        })

    return documents