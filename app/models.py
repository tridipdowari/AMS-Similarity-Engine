from pydantic import BaseModel


class ProposalInput(BaseModel):
    title: str = ""
    description: str = ""
    objectives: str = ""
    methodology: str = ""