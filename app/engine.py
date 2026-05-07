from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

from app.data import get_documents

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load proposal data
documents = get_documents()

# Extract proposal texts
proposal_texts = [doc["text"] for doc in documents]

# Generate embeddings
doc_embeddings = model.encode(proposal_texts)

# Convert to float32
doc_embeddings = np.array(doc_embeddings).astype("float32")

# Normalize vectors (important for cosine similarity)
faiss.normalize_L2(doc_embeddings)

# Vector dimension
dimension = doc_embeddings.shape[1]

# Create FAISS index using Inner Product
index = faiss.IndexFlatIP(dimension)

# Store vectors in FAISS
index.add(doc_embeddings)


def search_similar(query_text: str, top_k: int = 3):

    # Convert query → embedding
    query_vector = model.encode([query_text])

    # Convert to float32
    query_vector = np.array(query_vector).astype("float32")

    # Normalize query vector
    faiss.normalize_L2(query_vector)

    # Search similar vectors
    scores, indices = index.search(query_vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        matched_doc = documents[int(idx)]

        similarity_score = round(float(scores[0][i]) * 100, 2)
        if similarity_score < 30:
            continue

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