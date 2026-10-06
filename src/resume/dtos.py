from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, Dict, Literal, Optional

class ResumeStatusResponse(BaseModel):
    id: int
    status: str
    extracted_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
        

# Resume Structure  
class PersonalDetails(BaseModel):
    fullName: str
    jobTitle: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None

class EducationItem(BaseModel):
    id: str
    degree: str
    institution: str
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None
    highlights: list[str] = Field(default_factory=list)

class ExperienceBullet(BaseModel):
    id: Optional[int] = None
    text: str
    isInteractive: Optional[bool] = False

class WorkExperienceItem(BaseModel):
    id: str
    role: str
    company: str
    duration: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    location: Optional[str] = None
    bullets: list[ExperienceBullet] = Field(default_factory=list)

class ProjectItem(BaseModel):
    id: str
    title: str
    techStack: Optional[str] = None
    link: Optional[str] = None
    duration: Optional[str] = None
    bullets: list[str] = Field(default_factory=list)

class InternshipItem(BaseModel):
    id: str
    role: str
    company: str
    duration: Optional[str] = None
    location: Optional[str] = None
    bullets: list[str] = Field(default_factory=list)

class SkillCategory(BaseModel):
    category: str
    skills: list[str] = Field(default_factory=list)

class KeySkillsData(BaseModel):
    languages: list[str] = Field(default_factory=list)
    libraries: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    other: list[str] = Field(default_factory=list)
    categories: list[SkillCategory] = Field(default_factory=list)

class CertificationItem(BaseModel):
    id: str
    title: str
    issuer: str
    issueDate: Optional[str] = None
    credentialUrl: Optional[str] = None
    credentialId: Optional[str] = None

class SocialLink(BaseModel):
    platform: str
    url: str
    label: Optional[str] = None

class LanguageItem(BaseModel):
    name: str
    proficiency: Optional[str] = None

class ExtraCurricularItem(BaseModel):
    id: str
    title: str
    organization: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None

class LeadershipItem(BaseModel):
    id: str
    role: str
    organization: str
    duration: Optional[str] = None
    description: Optional[str] = None
    
class CustomSectionItem(BaseModel):
    id: str
    title: str
    subHeading: Optional[str] = None
    content: Optional[str] = None
    bullets: list[str] = Field(default_factory=list)


class ResumeData(BaseModel):
    personalDetails: Optional[PersonalDetails] = None
    profileSummary: Optional[str] = None
    education: list[EducationItem] = Field(default_factory=list)
    workExperience: list[WorkExperienceItem] = Field(default_factory=list)
    keySkills: Optional[KeySkillsData] = None
    projects: list[ProjectItem] = Field(default_factory=list)
    internships: list[InternshipItem] = Field(default_factory=list)
    certifications: list[CertificationItem] = Field(default_factory=list)
    socialLinks: list[SocialLink] = Field(default_factory=list)
    languages: list[LanguageItem] = Field(default_factory=list)
    hobbies: list[str] = Field(default_factory=list)
    extraCurricular: list[ExtraCurricularItem] = Field(default_factory=list)
    leadership: list[LeadershipItem] = Field(default_factory=list)
    customSections: list[CustomSectionItem] = Field(default_factory=list)
# End Of Resume Structure

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