from fastapi import FastAPI

from app.models import ProposalInput
from app.engine import search_similar

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AMS Similarity Engine Running"}


@app.post("/search")
def search(proposal: ProposalInput):

    # Combine proposal fields into one semantic query
    query_text = f"""
    {proposal.title}
    {proposal.introduction}
    {proposal.actionPlan}
    {proposal.expectedOutcome}
    {' '.join(proposal.objectives)}
    """

    # Run similarity search
    results = search_similar(query_text)

    return {
        "query_title": proposal.title,
        "total_matches": len(results),
        "results": results
    }