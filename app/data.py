from app.db import collection


def get_documents():

    docs = collection.find({})

    documents = []

    for d in docs:

        documents.append({
            "id": str(d.get("_id")),

            "title": d.get("title", ""),

            "discipline": d.get("discipline", ""),

            "introduction": d.get("introduction", ""),

            "actionPlan": d.get("actionPlan", ""),

            "expectedOutcome": d.get("expectedOutcome", ""),

            "objectives": d.get("objectives", [])
        })

    return documents