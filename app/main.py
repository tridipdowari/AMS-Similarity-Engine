from fastapi import FastAPI

from app.models import ProposalInput
from app.engine import search_similar, add_document

app = FastAPI()


@app.get("/")
def home():
    return {"message": "AMS Similarity Engine Running"}


@app.post("/search")
def search(proposal: ProposalInput):

    # Run similarity search
    results = search_similar({
        "title": proposal.title,
        "discipline": proposal.discipline,
        "introduction": proposal.introduction,
        "actionPlan": proposal.actionPlan,
        "expectedOutcome": proposal.expectedOutcome,
        "objectives": proposal.objectives
    })

    add_document({
        "id": abs(hash(proposal.title)),
        "title": proposal.title,
        "discipline": proposal.discipline,
        "introduction": proposal.introduction,
        "actionPlan": proposal.actionPlan,
        "expectedOutcome": proposal.expectedOutcome,
        "objectives": proposal.objectives
    })

    return {
        "query_title": proposal.title,
        "total_matches": len(results),
        "results": results
    }