from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class Experience(BaseModel):
    role: str = Field(description="Job title or designation")
    company: Optional[str] = Field(default=None, description="Company or organization name")
    start_date: Optional[str] = Field(default=None, description="Start date (e.g., 'Jan 2020)")
    end_date: Optional[str] = Field(default="Present", description="End Date or 'Present'")
    highlights: List[str] = Field(default_factory=list, description="EXHAUSTIVE list of ALL bullet points, responsibilities, and achievements for this role. Extract EVERY SINGLE bullet point or paragraph from this position without omitting, summarizing, or condensing any details.")
    
class StructuredResume(BaseModel):
    full_name: Optional[str] = Field(default=None, description="Candidate's full name")
    email: Optional[str] = Field(default=None, description="Candidate's contact email")
    total_years_experience: Optional[float] = Field(default=None,
        description="Estimated total years of professional experience across all roles"
    )
    hard_skills: List[str] = Field(default_factory=list, description="Technical tools, languages, platforms")
    soft_skills: List[str] = Field(default_factory=list, description="Interpersonal abilities and soft skills")
    work_experience: List[Experience] = Field(default_factory=list)
    # education: List[]