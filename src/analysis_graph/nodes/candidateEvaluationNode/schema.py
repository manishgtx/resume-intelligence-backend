from typing import List, Optional, Literal, Dict, Union
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class BaseFitLensModel(BaseModel):
    """Base model configured to serialize Python snake_case to frontend camelCase."""
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True
    )


# --- METRICS ---
class FitLensMetrics(BaseFitLensModel):
    match_score: int = Field(..., ge=0, le=100, description="Overall match percentage (0-100)")
    matched_count: int = Field(..., ge=0, description="Count of requirements fully met")
    underperforming_count: int = Field(..., ge=0, description="Count of partial/weak requirements")
    missing_count: int = Field(..., ge=0, description="Count of hard missing requirements")


# --- REQUIREMENTS ---
class RequirementItem(BaseFitLensModel):
    id: str = Field(..., description="Unique ID, e.g. 'req-1'")
    index: int = Field(..., description="Display index, e.g. 1, 2, 3")
    title: str = Field(..., description="Extracted requirement text")
    subtitle: str = Field(..., description="Context label, e.g. 'Core requirement', 'High impact'")
    status: Literal["missing", "met", "partial"]
    status_label: str = Field(..., description="'Missing', 'Met', or 'Partial'")
    category: Literal["must-have", "key-deliverable", "buried-signal"]
    target_line: int = Field(..., description="Estimated line number (1-40) in resume gutter")
    color: Literal["red", "green", "amber"] = Field(..., description="'green' for met, 'amber' for partial, 'red' for missing")


class JobRequirements(BaseFitLensModel):
    must_haves: List[RequirementItem] = Field(default_factory=list)
    key_deliverables: List[RequirementItem] = Field(default_factory=list)
    buried_signals: List[RequirementItem] = Field(default_factory=list)


# --- COACH INSIGHTS ---
class CoachSuggestionVariant(BaseFitLensModel):
    type: Literal["metrics", "technical", "leadership"]
    title: str = Field(..., description="Variant title, e.g. 'Suggested (Metrics-first)'")
    suggested_text: str = Field(..., description="Rewritten bullet text")
    tags: List[str] = Field(default_factory=list, description="Tags, e.g. ['Scale', 'Impact', 'Tools']")


class CoachInsight(BaseFitLensModel):
    bullet_id: int = Field(..., description="Maps to ExperienceBullet.id (e.g. 1, 2, 3)")
    line_context: str = Field(..., description="E.g. 'Selected: ① • Bullet under Experience'")
    current_text: str = Field(..., description="Original bullet text from candidate's resume")
    feedback: str = Field(..., description="Critique explaining why this bullet is weak or vague")
    why_it_matters: str = Field(..., description="Why recruiters/ATS scan for this dimension")
    variants: Dict[Literal["metrics", "technical", "leadership"], CoachSuggestionVariant]


# --- MISSING GAPS ---
class MissingSkill(BaseFitLensModel):
    id: str = Field(..., description="Unique ID, e.g. 'skill-1'")
    title: str = Field(..., description="Missing keyword/tool, e.g. 'CI/CD Pipeline'")
    mentions: int = Field(..., ge=1, description="Times mentioned in JD")
    type: Literal["skill", "experience", "summary"]
    category_label: str = Field(..., description="Domain label, e.g. 'DevOps & Tooling'")
    recommended_placement: Literal["skills", "experience", "summary"]
    target_role: Optional[str] = Field(None, description="Role name to append to if type is experience")
    suggested_bullet: Optional[str] = Field(None, description="Ready-to-use bullet point incorporating this skill")


# --- PARSED RESUME ---
class PersonalDetails(BaseFitLensModel):
    full_name: str
    job_title: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    github: Optional[str] = None


class EducationItem(BaseFitLensModel):
    id: str
    degree: str
    institution: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None


class ExperienceBullet(BaseFitLensModel):
    id: Optional[int] = Field(None, description="Integer ID (1, 2, 3...) if this bullet has coach suggestions")
    text: str
    is_interactive: Optional[bool] = Field(False, description="Set True if linked to a CoachInsight")


class WorkExperienceItem(BaseFitLensModel):
    id: str
    role: str
    company: str
    duration: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    bullets: List[Union[ExperienceBullet, str]] = Field(default_factory=list)


class SkillCategory(BaseFitLensModel):
    category: str
    skills: List[str]


class KeySkillsData(BaseFitLensModel):
    languages: Optional[List[str]] = Field(default_factory=list)
    libraries: Optional[List[str]] = Field(default_factory=list)
    tools: Optional[List[str]] = Field(default_factory=list)
    other: Optional[List[str]] = Field(default_factory=list)
    categories: Optional[List[SkillCategory]] = None


class ProjectItem(BaseFitLensModel):
    id: str
    title: str
    tech_stack: Optional[str] = None
    link: Optional[str] = None
    duration: Optional[str] = None
    bullets: Optional[List[str]] = Field(default_factory=list)


class InternshipItem(BaseFitLensModel):
    id: str
    role: str
    company: str
    duration: Optional[str] = None
    location: Optional[str] = None
    bullets: Optional[List[str]] = Field(default_factory=list)


class CertificationItem(BaseFitLensModel):
    id: str
    title: str
    issuer: str
    issue_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class LanguageItem(BaseFitLensModel):
    name: str
    proficiency: Optional[str] = None


class LeadershipItem(BaseFitLensModel):
    id: str
    role: str
    organization: str
    duration: Optional[str] = None
    description: Optional[str] = None


class ExtraCurricularItem(BaseFitLensModel):
    id: str
    title: str
    organization: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None


class CustomSectionItem(BaseFitLensModel):
    id: str
    title: str
    sub_heading: Optional[str] = None
    content: Optional[str] = None
    bullets: Optional[List[str]] = None


class ResumeData(BaseFitLensModel):
    personal_details: Optional[PersonalDetails] = None
    profile_summary: Optional[str] = None
    work_experience: Optional[List[WorkExperienceItem]] = Field(default_factory=list)
    education: Optional[List[EducationItem]] = Field(default_factory=list)
    key_skills: Optional[KeySkillsData] = None
    projects: Optional[List[ProjectItem]] = Field(default_factory=list)
    internships: Optional[List[InternshipItem]] = Field(default_factory=list)
    certifications: Optional[List[CertificationItem]] = Field(default_factory=list)
    languages: Optional[List[LanguageItem]] = Field(default_factory=list)
    leadership: Optional[List[LeadershipItem]] = Field(default_factory=list)
    extra_curricular: Optional[List[ExtraCurricularItem]] = Field(default_factory=list)
    hobbies: Optional[List[str]] = Field(default_factory=list)
    custom_sections: Optional[List[CustomSectionItem]] = Field(default_factory=list)


# --- ROOT RESPONSE OBJECT ---
class EvaluationOutput(BaseFitLensModel):
    """Pass this root model directly to OpenAI .parse() or LangChain .with_structured_output()."""
    metrics: FitLensMetrics
    requirements: JobRequirements
    resume_data: ResumeData
    coach_insights: Dict[str, CoachInsight] = Field(
        ..., 
        description="Map of coach insights where keys are string IDs: '1', '2', '3'"
    )
    missing_skills: List[MissingSkill] = Field(default_factory=list)
