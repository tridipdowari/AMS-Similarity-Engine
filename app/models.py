from pydantic import BaseModel
from typing import List


class ProposalInput(BaseModel):
    title: str
    introduction: str
    actionPlan: str
    expectedOutcome: str
    objectives: List[str]