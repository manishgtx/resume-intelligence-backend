from enum import Enum
from datetime import datetime
from typing import Any, Optional, List
from pydantic import BaseModel, ConfigDict, Field

class JobDescription(BaseModel):
    title: str
    description: str
    company: str
    
class JobStatus(str, Enum):
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    title: str
    description: str
    company: str
    result: Optional[dict[str, Any]] = None
    errorMessage: Optional[str] = None
    status: JobStatus
    is_verified: bool
    created_at: datetime
    verified_at: Optional[datetime] = None
    
# Schema For Model
class SkillType(str, Enum):
    SKILL = "skill"
    EXPERIENCE = "experience"


class Level(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"


class MustHave(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Sequential id: mh_1, mh_2")
    title: str = Field(description="One atomic requirement, concise, max 15 words")
    subtitle: str = Field(description="Short label, e.g. 'Core requirement', 'Company priority'")
    category: str = Field(default="must-have")
    keywords: List[str] = Field(description="Normalized skills/tools/terms for matching against a resume")
    aliases: List[str] = Field(default_factory=list, description="Synonyms and alternate spellings, e.g. 'TS' for TypeScript")
    min_years: Optional[int] = Field(default=None, alias="minYears")
    evidence: str = Field(description="Exact JD sentence or fragment this was derived from")


class KeyDeliverable(BaseModel):
    id: str = Field(description="Sequential id: kd_1, kd_2")
    title: str = Field(description="One atomic thing the person will build, ship or own, max 15 words")
    subtitle: str = Field(description="Short label, e.g. 'High impact', 'Day-to-day'")
    category: str = Field(default="key-deliverable")
    keywords: List[str]
    evidence: str = Field(description="Exact JD sentence or fragment this was derived from")


class BuriedSignal(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Sequential id: bs_1, bs_2")
    signal: str = Field(description="Implicit expectation, e.g. 'Expects ownership with minimal supervision'")
    evidence: str = Field(description="Exact JD phrase that implies it")
    resume_hint: str = Field(alias="resumeHint", description="What resume evidence would prove it")


class MissingSkill(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(description="Normalized skill or experience name, e.g. 'CI/CD Pipeline'")
    type: SkillType = Field(description="'skill' for tools/technologies, 'experience' for practices/exposure")
    level: Level = Field(description="'required' or 'preferred' as framed in the JD")
    aliases: List[str] = Field(default_factory=list, description="Synonyms and alternate spellings used for matching")
    mentions: int = Field(ge=1, description="Times mentioned or clearly implied in the JD")
    in_must_have: bool = Field(alias="inMustHave")


class StructuredJD(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    must_haves: List[MustHave] = Field(alias="mustHaves")
    key_deliverables: List[KeyDeliverable] = Field(alias="keyDeliverables")
    buried_signals: List[BuriedSignal] = Field(alias="buriedSignals")
    missing_skills: List[MissingSkill] = Field(alias="missingSkills")