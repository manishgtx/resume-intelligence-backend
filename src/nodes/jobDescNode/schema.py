from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class WorkLocationType(str, Enum):
    REMOTE = "Remote"
    HYBRID = "Hybrid"
    ON_SITE = "On-site"
    UNSPECIFIED = "Unspecified"
    
class EmploymentType(str, Enum):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    CONTRACT = "Contract"
    INTERNSHIP = "Internship"
    TEMPORARY = "Temporary"
    UNSPECIFIED = "Unspecified"
    
class MandatoryRequirements(BaseModel):
     hard_skills: List[str] = Field(
         default_factory=list,
         description="Atomized list of mandatory technical skills, languages, frameworks, or tools."
     )
     minimum_years_experience: Optional[int] = Field(
         default=None,
         description="Minimum numeric years of experience explicityly required."
     )
     education_degrees: List[str] = Field(
         default_factory=list,
         description="Required degrees or minimum educational levels (e.g., Bachelor's in CSE)"
     )
     certification_licenses: List[str] = Field(
         default_factory=list,
         description="Mandatory certifications, licenses, or clearances (e.g., AWS Solutions Architect, PMP)."
     )
     
class PreferredQualifications(BaseModel):
    hard_skills: List[str] = Field(
        default_factory=list,
        description="Nice-to-have technical skills or tools."
    )
    domain_knowledge: List[str] = Field(
        default_factory=list,
        description="Preferred domain, industry, or sector experience (e.g., FinTech, Healthcare)"
    )
    soft_skills: List[str] = Field(
        default_factory=list,
        description="Interpersonal skills, leadership traits, or work styles mentioned."
    )
    
class JobDescriptionData(BaseModel):
    # job_title: str = Field(description="Exact or core job title.")
    # seniority_level: Optional[str] = Field(
    #     default=None,
    #     description="e.g., Entry-level, Mid-Senior, Lead, Director."
    # )
    # department: Optional[str] = Field(default=None, description="Department or business unit.")
    # work_location_type: WorkLocationType = Field(default=WorkLocationType.UNSPECIFIED)
    # employment_type: EmploymentType = Field(default=EmploymentType.UNSPECIFIED)
    
    mandatory_requirements: MandatoryRequirements
    # preferred_qualifications: PreferredQualifications
    
    # key_responsibilities: List[str] = Field(
    #     default_factory=list,
    #     description="List of core daily duties, objectives, or responsibilities."
    # )
    
    
    # {'job_title': 'Search Engineer',
    #  'seniority_level': 'Mid-Senior',
    #  'department': 'Engineering - Software & QA',
    #  'employment_type': 'Full-time',
    #  'preferred_qualifications': {
    #      'hard_skills': ['Java', 'Git', 'continuous integration', 'continuous delivery',
    #                      'LLM', 'RAG pipelines', 'model evaluation', 'anomaly detection'],
    #      'domain_knowledge': ['fintech', 'distributed systems', 'databases', 'security', 'front-end'],
    #      'soft_skills': ['leadership', 'communication', 'cross-functional collaboration']
    #      }
    #  }