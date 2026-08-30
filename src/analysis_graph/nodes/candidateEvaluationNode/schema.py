# from pydantic import BaseModel, Field

from pydantic import BaseModel, Field


class evaluation(BaseModel):
    reasoning: str = Field(
        description="Brief explanation of why the candidate passed/failed eligibility and earned this score."
    )
    basic_eligibility: bool = Field(
        description="True if all hard criteria are met, False otherwise."
    )
    score: int = Field(
        description="Match score from 1 to 100 based on fit.", ge=1, le=100
    )