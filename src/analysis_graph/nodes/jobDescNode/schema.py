from enum import Enum
from pydantic import BaseModel

class RequirementCategory(str, Enum):
    REQUIRED_SKILL = "required_skill"
    PREFERRED_SKILL = "preferred_skill"
    EXPERIENCE = "experience"
    EDUCATION = "education"

class JDRequirements(BaseModel):
    requirement: str
    category: RequirementCategory
    mandatory: bool
    
class StructuredJD(BaseModel):
    requirement: list[JDRequirements]