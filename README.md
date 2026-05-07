# AMS Similarity Engine

## Overview

AMS Similarity Engine is a semantic proposal similarity detection system built using:

* FastAPI
* Sentence Transformers
* FAISS
* MongoDB

The system compares incoming project proposals with existing proposals stored in MongoDB and returns semantically similar matches using vector embeddings.

---

# Features

* Semantic similarity search
* MongoDB integration
* FAISS vector indexing
* REST API using FastAPI
* Real-time proposal comparison
* Similarity score classification

---

# Tech Stack

| Technology            | Purpose                  |
| --------------------- | ------------------------ |
| FastAPI               | Backend API              |
| Sentence Transformers | Text embeddings          |
| FAISS                 | Vector similarity search |
| MongoDB               | Proposal storage         |
| PyMongo               | MongoDB connection       |
| Uvicorn               | FastAPI server           |

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

1. Existing proposals are stored in MongoDB.
2. Similarity engine fetches proposal data from MongoDB.
3. Semantic embeddings are generated using SentenceTransformer.
4. FAISS creates vector indexes for fast similarity search.
5. Backend sends a new proposal to the `/search` API route.
6. Similarity engine compares the new proposal with existing proposals.
7. Similarity scores and matched proposals are returned.

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

# Similarity Classification

| Score Range | Status |
| ----------- | ------ |
| 80+         | HIGH   |
| 50 - 79     | MEDIUM |
| Below 50    | LOW    |

---

# How Similarity Works

The system uses SentenceTransformer embeddings to convert proposal text into dense vectors.

FAISS performs cosine similarity search between:

* Incoming proposal embedding
* Existing proposal embeddings

The most semantically similar proposals are returned with similarity scores.

---

# Future Improvements

* Persistent FAISS index storage
* Incremental vector updates
* Hybrid semantic + keyword search
* Async indexing pipeline
* Better ranking algorithms
* Proposal exclusion logic

---

# Author

Tridip Dowari
