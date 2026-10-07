from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Literal, Optional,List

class ResumeStatusResponse(BaseModel):
    id: int
    status: str
    extracted_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        
# Resume Model
class PersonalDetails(BaseModel):
    fullName: str = Field(description="Candidate's full name")
    jobTitle: Optional[str] = Field(None, description="Current or target headline title")
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = Field(None, description="City, Country")
    linkedin: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None
    
class WorkExperienceItem(BaseModel):
    role: str
    company: str
    duration: Optional[str] = Field(None, description="e.g. 'Sep 2023 – Aug 2025'")
    location: Optional[str] = None
    bullets: List[str] = Field(
        description="Individual accomplishment bullets. Each bullet must be an actionable accomplishment or responsibility."
    )
    
class EducationItem(BaseModel):
    degree: str
    institution: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    
class KeySkillsData(BaseModel):
    languages: List[str] = Field(default_factory=list, description="e.g. TypeScript, Python, SQL")
    libraries: List[str] = Field(default_factory=list, description="e.g. React, Next.js, Redux, FastAPI")
    tools: List[str] = Field(default_factory=list, description="e.g. Git, Docker, Jest, Vite")
    other: List[str] = Field(default_factory=list, description="Additional tools or domain expertise")
    
class ProjectItem(BaseModel):
    title: str
    techStack: Optional[str] = None
    link: Optional[str] = None
    duration: Optional[str] = None
    bullets: List[str] = Field(default_factory=list)
    
class CertificationItem(BaseModel):
    title: str
    issuer: str
    issueDate: Optional[str] = None
    credentialId: Optional[str] = None
    
class LanguageItem(BaseModel):
    name: str
    proficiency: Optional[str] = None
    
# Master Model for the 1st LLM Call
class ResumeData(BaseModel):
    personalDetails: PersonalDetails
    profileSummary: Optional[str] = None
    workExperience: List[WorkExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    keySkills: KeySkillsData = Field(default_factory=KeySkillsData)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[CertificationItem] = Field(default_factory=list)
    languages: List[LanguageItem] = Field(default_factory=list)
    hobbies: List[str] = Field(default_factory=list)
# End Of Resume Model

# Data Layer
class ResumeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int] = None
    filename: str
    status: Literal["processing", "draft", "failed", "verified"]
    is_verified: bool
    extracted_data: Optional[dict[str, Any]] = None
    created_at: datetime
    verified_at: Optional[datetime] = None

class ResumeDetailOut(ResumeOut):
    raw_text: Optional[str] = None