# AMS Similarity Engine

## Overview

AMS Similarity Engine is a semantic proposal similarity detection system built using:

* FastAPI
* Sentence Transformers
* FAISS
* Qdrant
* MongoDB

The system compares incoming project proposals with existing proposals stored in MongoDB and returns semantically similar matches using vector embeddings.

---

# Features

* Semantic proposal similarity detection
* SentenceTransformer embedding generation
* Qdrant vector database integration
* FAISS cosine similarity retrieval
* MongoDB proposal storage
* Automatic vector synchronization recovery
* Real-time proposal comparison
* Threshold-based similarity classification
* FastAPI REST API

---

# Tech Stack

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| FastAPI               | Backend API               |
| Sentence Transformers | Text embeddings           |
| FAISS                 | Vector similarity search  |
| MongoDB               | Proposal storage          |
| PyMongo               | MongoDB connection        |
| Uvicorn               | FastAPI server            |
| Qdrant                |Persistent vector database |

---

# Project Structure

```bash
AMS-Similarity-Engine/
│
├── app/
│   ├── main.py
│   ├── engine.py
│   ├── data.py
│   ├── db.py
│   └── models.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# Workflow

1. Proposals are stored in MongoDB.
2. Proposal text fields are combined into a single semantic document.
3. SentenceTransformer generates dense vector embeddings.
4. Embeddings are stored in Qdrant vector database.
5. Existing vectors are loaded into FAISS for fast cosine similarity retrieval.
6. Incoming proposals are converted into embeddings during API requests.
7. FAISS performs semantic similarity search against existing proposal vectors.
8. Similarity scores are classified as HIGH, MEDIUM, or LOW.
9. If Qdrant vectors become inconsistent with MongoDB, the engine automatically rebuilds vectors during startup synchronization.

---

# MongoDB Structure

## Database

```text
test
```

## Collection

```text
projects
```

## Proposal Fields Used

* title
* introduction
* actionPlan
* expectedOutcome
* objectives

---

# Installation

## Clone Repository

```bash
git clone <repository-link>
cd AMS-Similarity-Engine
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
```

---

## Activate Virtual Environment

### Mac/Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Server

```bash
uvicorn app.main:app --reload
```

Server runs at:

```text
http://127.0.0.1:8000
```

Swagger API Docs:

```text
http://127.0.0.1:8000/docs
```

---

# API Endpoint

## Search Similar Proposals

### Route

```http
POST /search
```

---

## Request Body

```json
{
  "title": "AI attendance tracking system",
  "introduction": "Automated attendance using facial recognition",
  "actionPlan": "Train facial recognition model and deploy attendance system",
  "expectedOutcome": "Reduce manual attendance errors",
  "objectives": [
    "Automate attendance tracking",
    "Improve classroom monitoring"
  ]
}
```

---

## Example Response

```json
{
  "query_title": "AI attendance tracking system",
  "total_matches": 1,
  "results": [
    {
      "proposal_id": "69fc345e3f497400673c2ab1",
      "title": "AI Based Smart Attendance System",
      "similarity_score": 87.14,
      "status": "HIGH"
    }
  ]
}
```

---

# How Similarity Works

The system uses SentenceTransformer embeddings to convert proposal content into dense semantic vectors.

Cosine similarity is used to measure semantic overlap between:
- incoming proposals
- existing proposal vectors

FAISS performs high-speed nearest-neighbor retrieval while Qdrant stores persistent vector embeddings.

The similarity engine classifies proposals using threshold-based semantic similarity rules:

| Score | Classification |
|-------|----------------|
| ≥ 80  | HIGH           |
| 50–79 | MEDIUM         |
| < 50  | LOW            |

---

# Future Improvements

* Distributed vector scaling
* Advanced proposal ranking
* Hybrid semantic + keyword retrieval
* Proposal deletion synchronization
* Fine-tuned domain-specific embedding models
* Authentication and access control

---

# Author

Tridip Dowari
