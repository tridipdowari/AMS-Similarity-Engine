from pydantic import BaseModel
from typing import List


class ProposalInput(BaseModel):
    id: str
    title: str
    discipline: str
    introduction: str
    actionPlan: str
    expectedOutcome: str
    objectives: List[str]