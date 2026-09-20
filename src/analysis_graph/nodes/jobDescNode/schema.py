from typing import List, Literal
from pydantic import BaseModel, Field

RequirementPriority = Literal["must_have", "nice_to_have", "bonus_preferred"]

class JDCriterion(BaseModel):
    id: str = Field(
        description="Unique ID starting sequentially from 'crit_1'"
    )
    category: str = Field(
        description="Functional category, e.g., 'Technical Skills', 'Experience', 'Education', 'Soft Skills'"
    )
    priority: RequirementPriority = Field(
        description="Weight of requirement: 'must_have' (strict minimum requirement), 'nice_to_have' (valuable addition), or 'bonus_preferred' (extra credit / stand-out qualification)"
    )
    requirement: str = Field(
        description="Atomic, single requirement text. Do not bundle multiple skills together."
    )

class JobDescriptionExtraction(BaseModel):
    criteria: List[JDCriterion]