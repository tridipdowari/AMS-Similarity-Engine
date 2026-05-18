import os
import faiss
import numpy as np

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from app.data import get_documents
from app.db import collection

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    timeout=60
)

COLLECTION_NAME = "research_proposals"

collections = client.get_collections().collections

collection_names = [collection.name for collection in collections]

if COLLECTION_NAME not in collection_names:

    client.create_collection(
        collection_name=COLLECTION_NAME,

        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("Qdrant collection created.")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384

faiss_index = faiss.IndexFlatIP(dimension)

faiss_id_map = []

def generate_embedding(text):

    embedding = model.encode(text)

    embedding = np.array(embedding).astype("float32")

    norm = np.linalg.norm(embedding)

    if norm > 0:
        embedding = embedding / norm

    return embedding.tolist()

documents = get_documents()

mongo_count = collection.count_documents({})

qdrant_count = client.count(
    collection_name=COLLECTION_NAME,
    exact=True
).count

print("Mongo Count:", mongo_count)
print("Qdrant Count:", qdrant_count)

if mongo_count != qdrant_count:

    print("MongoDB and Qdrant out of sync. Rebuilding vectors...")

    client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )

    print("Uploading documents to Qdrant...")

    points = []

    for i, doc in enumerate(documents):

        combined_text = f"""
        TITLE:
        {doc.get("title", "")}

        DISCIPLINE:
        {doc.get("discipline", "")}

        INTRODUCTION:
        {doc.get("introduction", "")}

        OBJECTIVES:
        {' '.join(doc.get("objectives", []))}

        ACTION PLAN:
        {doc.get("actionPlan", "")}

        EXPECTED OUTCOME:
        {doc.get("expectedOutcome", "")}
        """

        embedding = generate_embedding(combined_text)

        payload = {

            "id": doc.get("id"),

            "title": doc.get("title", ""),

            "discipline": doc.get("discipline", "").strip().lower(),

            "introduction": doc.get("introduction", ""),

            "actionPlan": doc.get("actionPlan", ""),

            "expectedOutcome": doc.get("expectedOutcome", ""),

            "objectives": doc.get("objectives", [])
        }

        points.append(
            PointStruct(
                id=i,
                vector=embedding,
                payload=payload
            )
        )

    BATCH_SIZE = 5

    for i in range(0, len(points), BATCH_SIZE):

        batch = points[i:i + BATCH_SIZE]

        client.upsert(
            collection_name=COLLECTION_NAME,
            points=batch
        )

    print("Documents uploaded to Qdrant.")

# =========================
# LOAD EXISTING QDRANT DATA INTO FAISS
# =========================

faiss_index.reset()

faiss_id_map.clear()

stored_points = client.scroll(
    collection_name=COLLECTION_NAME,
    limit=1000,
    with_vectors=True,
    with_payload=True
)[0]

if len(stored_points) > 0:

    all_vectors = []

    faiss_id_map.clear()

    for point in stored_points:

        vector = np.array(point.vector).astype("float32")

        all_vectors.append(vector)

        faiss_id_map.append(point.payload)

    all_vectors = np.array(all_vectors)

    faiss.normalize_L2(all_vectors)

    faiss_index.add(all_vectors)

    print("Existing vectors loaded into FAISS.")

def search_similar(query_data, top_k: int = 3):

    combined_query = f"""
    TITLE:
    {query_data.get("title", "")}

    DISCIPLINE:
    {query_data.get("discipline", "")}

    INTRODUCTION:
    {query_data.get("introduction", "")}

    OBJECTIVES:
    {' '.join(query_data.get("objectives", []))}

    ACTION PLAN:
    {query_data.get("actionPlan", "")}

    EXPECTED OUTCOME:
    {query_data.get("expectedOutcome", "")}
    """

    query_vector = generate_embedding(combined_query)

    query_vector = np.array([query_vector]).astype("float32")

    faiss.normalize_L2(query_vector)

    scores, indices = faiss_index.search(query_vector, top_k)

    results = []

    for idx, score in zip(indices[0], scores[0]):

        if idx == -1:
            continue

        matched_doc = faiss_id_map[idx]

        similarity_score = round(float(score) * 100, 2)

        if similarity_score >= 80:
            status = "HIGH"

        elif similarity_score >= 50:
            status = "MEDIUM"

        else:
            status = "LOW"

        results.append({

            "proposal_id": matched_doc["id"],

            "title": matched_doc["title"],

            "similarity_score": max(similarity_score, 0),

            "status": status
        })

    return results


def add_document(new_doc):

    global documents

    text = f"""
    TITLE:
    {new_doc.get("title", "")}

    DISCIPLINE:
    {new_doc.get("discipline", "")}

    INTRODUCTION:
    {new_doc.get("introduction", "")}

    OBJECTIVES:
    {' '.join(new_doc.get("objectives", []))}

    ACTION PLAN:
    {new_doc.get("actionPlan", "")}

    EXPECTED OUTCOME:
    {new_doc.get("expectedOutcome", "")}
    """

    embedding = generate_embedding(text)

    vector = np.array([embedding]).astype("float32")

    faiss.normalize_L2(vector)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": int(new_doc.get("id")),
                "vector": embedding,
                "payload": {
                    "id": new_doc.get("id"),
                    "title": new_doc.get("title", ""),
                    "discipline": new_doc.get("discipline", ""),
                    "introduction": new_doc.get("introduction", ""),
                    "actionPlan": new_doc.get("actionPlan", ""),
                    "expectedOutcome": new_doc.get("expectedOutcome", ""),
                    "objectives": new_doc.get("objectives", []),
                }
            }
        ]
    )

    faiss_index.add(vector)

    faiss_id_map.append({
        "id": str(new_doc.get("_id", new_doc.get("id"))),
        "title": new_doc.get("title", ""),
        "discipline": new_doc.get("discipline", "").strip().lower(),
        "introduction": new_doc.get("introduction", ""),
        "actionPlan": new_doc.get("actionPlan", ""),
        "expectedOutcome": new_doc.get("expectedOutcome", ""),
        "objectives": new_doc.get("objectives", [])
    })

    # Store document in memory
    documents.append({

    "id": new_doc.get("id"),

    "title": new_doc.get("title", ""),

    "discipline": new_doc.get("discipline", "").strip().lower(),

    "introduction": new_doc.get("introduction", ""),

    "actionPlan": new_doc.get("actionPlan", ""),

    "expectedOutcome": new_doc.get("expectedOutcome", ""),

    "objectives": new_doc.get("objectives", [])
})