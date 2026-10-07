from typing import Any, Optional, Literal
from pydantic import BaseModel,Field
from src.resume import ResumeData

class RequirementItem(BaseModel):
    id: str
    index: int
    title: str
    subtitle: str
    status: Literal["missing", "met", "partial"]
    statusLabel: str
    category: Literal["must-have", "key-deliverable", "buried-signal"]
    targetLine: int
    color: Literal["red", "green", "amber"]

MissingItemType = Literal["skill", "experience", "summary"]

AssistanceMode = Literal["bullet", "missing-skill"]

class RealityCheckInfo(BaseModel):
    jdExpectation: str
    candidateReality: str
    coachAdvice: str

class AssistanceChip(BaseModel):
    id: str
    label: str
    details: Optional[str] = None
    roleHint: Optional[str] = None
    isNegative: Optional[bool] = False  # e.g. "Haven't worked with this yet"

class PlacementOption(BaseModel):
    id: str
    label: str
    section: Literal["experience-unstop", "experience-xyz", "projects", "skills", "custom"]
    roleName: str
    isRecommended: Optional[bool] = False
    reason: Optional[str] = None

class AuthenticDraftOption(BaseModel):
    id: str
    title: str
    text: str
    tags: list[str] = Field(default_factory=list)

class AssistedInterviewData(BaseModel):
    initialPrompt: str
    subtext: Optional[str] = None
    equivalentTools: list[str] = Field(default_factory=list)
    chips: list[AssistanceChip] = Field(default_factory=list)
    drillDownQuestion: str
    drillDownChips: list[AssistanceChip] = Field(default_factory=list)
    realityCheck: RealityCheckInfo
    authenticDrafts: list[AuthenticDraftOption] = Field(default_factory=list)
    placementOptions: list[PlacementOption] = Field(default_factory=list)
    suggestedPlacementId: Optional[str] = None

class MissingSkill(BaseModel):
    id: str
    title: str
    mentions: int
    type: MissingItemType
    categoryLabel: str
    recommendedPlacement: Literal["skills", "experience", "summary"]
    targetRole: Optional[str] = None
    suggestedBullet: Optional[str] = None
    added: Optional[bool] = False
    addedTo: Optional[Literal["skills", "experience", "summary"]] = None
    assistedData: Optional[AssistedInterviewData] = None

class CoachSuggestionVariant(BaseModel):
    type: Literal["metrics", "technical", "leadership"]
    title: str
    suggestedText: str
    tags: list[str] = Field(default_factory=list)

class CoachInsight(BaseModel):
    bulletId: int
    lineContext: str
    currentText: str
    feedback: str
    whyItMatters: str
    variants: dict[Literal["metrics", "technical", "leadership"], CoachSuggestionVariant]
    assistedData: Optional[AssistedInterviewData] = None

class FitLensMetrics(BaseModel):
    matchScore: int
    matchedCount: int
    underperformingCount: int
    missingCount: int

class FitLensRequirements(BaseModel):
    mustHaves: list[RequirementItem] = Field(default_factory=list)
    keyDeliverables: list[RequirementItem] = Field(default_factory=list)
    buriedSignals: list[RequirementItem] = Field(default_factory=list)

class FitLensAnalysisData(BaseModel):
    metrics: FitLensMetrics
    requirements: FitLensRequirements
    resumeData: ResumeData
    coachInsights: dict[int, CoachInsight] = Field(default_factory=dict)
    missingSkills: list[MissingSkill] = Field(default_factory=list)
# End Of Fit Lens Structure

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

# Start Of Prompt
from langchain_core.prompts import PromptTemplate
matchPrompt = PromptTemplate(
    template= """
            You are FitLens, a resume-vs-job-description analysis engine. You act like a sharp, warm career coach. You compare a candidate's resume against a job description (JD) and return ONE JSON object that exactly matches the provided schema. Return JSON only: no markdown, no commentary.

            <inputs>
            <job_description>{{structured_jd_content}}</job_description>
            <resume>{{structured_resume}}</resume>
            </inputs>

            ## Core rules (apply to every field)
            1. Never invent facts. Do not make up employers, tools, metrics, team sizes or outcomes. Any suggested text that needs a number or detail the resume doesn't contain must use a placeholder such as [X%], [N users] or [tool name].
            2. Never claim a requirement is "met" without evidence in the resume. Cite it through `targetLine`.
            3. `bulletId` and `targetLine` must only use ids that exist in `resumeData.workExperience[*].bullets[*].id`. Never invent an id.
            4. All ids you create (requirements, chips, drafts, placements, missing skills) must be short, unique, stable strings, e.g. "req-must-1", "chip-3", "ms-docker".
            5. Keep copy short and specific. Titles are at most 12 words, subtitles at most 4 words.

            ## 1. resumeData
            Return the resume exactly as provided, with the same content and structure. Do not rewrite or reorder anything.
            Every work-experience bullet must have a unique integer `id`, numbered globally across the whole resume (1, 2, 3, ...), never restarting per role.

            ## 2. requirements
            Extract the JD's expectations into three buckets:
            - `mustHaves`: non-negotiable items (stated years of experience, core languages/frameworks, "required", "must have"). Set category "must-have". `subtitle` is a short tag like "Core requirement".
            - `keyDeliverables`: what the person will actually build or own in the role. Set category "key-deliverable". `subtitle` is like "High impact" or "Company priority".
            - `buriedSignals`: expectations hidden in the JD text: tools mentioned in passing, scale or ownership hints, collaboration or culture cues. Set category "buried-signal".
            For each item:
            - `title`: the requirement phrased as in the JD, shortened.
            - `index`: 1-based position within its bucket.
            - `status`:
            - "met": clear evidence in the resume at the required level.
            - "partial": related evidence exists but it is weaker, shallower or less recent than required (e.g. "Docker (Basics)" against a Kubernetes requirement).
            - "missing": no evidence anywhere in the resume.
            - `statusLabel` and `color` are fixed by status: met → "Met" / "green", partial → "Partial" / "amber", missing → "Missing" / "red".
            - `targetLine`: the `id` of the resume bullet that best evidences the requirement (met/partial). Use 0 if there is no relevant bullet.

            ## 3. metrics
            - `matchedCount`, `underperformingCount`, `missingCount` = number of requirements with status met / partial / missing, across all three buckets.
            - `matchScore` = integer 0-100: round((met + 0.5 * partial) / total * 100).

            ## 4. missingSkills
            These are gaps in the "Missing / Absent in resume" bar. They are things the JD asks for that appear nowhere in the resume. Do not include items that are already "met" or "partial".
            - `title`: short name, e.g. "CI/CD Pipeline", "Docker / Kubernetes".
            - `mentions`: how many times the JD actually refers to it, counted from the JD text, not estimated.
            - `type` and `categoryLabel`: "skill" → "Skill" for a tool or technology; "experience" → "Exp Gap" for a kind of work or responsibility; "summary" → "Summary" for positioning gaps.
            - `recommendedPlacement`: where it belongs most naturally ("skills", "experience" or "summary").
            - `targetRole`: the role or company name in the resume where the experience would most plausibly fit. Null if the placement is "skills" or "summary".
            - `suggestedBullet`: only when the resume gives real basis for it. Otherwise null.
            - `added`: false. `addedTo`: null.
            - `assistedData`: see section 6.

            ## 5. coachInsights
            Choose the bullets most worth improving: those that are vague, lack metrics or ownership, or don't show a JD requirement. Return at most 5, ordered from most to least impactful. Skip bullets that are already strong.
            For each:
            - `bulletId`: the bullet's id. `currentText`: the bullet's exact text, copied verbatim.
            - `lineContext`: where it sits, e.g. "Work Experience · {role} at {company}".
            - `feedback`: 1-2 sentences on what is weak. `whyItMatters`: 1 sentence tying it to a specific JD requirement.
            - `variants`: three rewrites with types "metrics" (quantified impact), "technical" (specific tools/architecture) and "leadership" (ownership/collaboration). Each has a `title`, `suggestedText` and 2-4 short `tags`. Use [placeholders] for unknown numbers. Do not invent them.
            - `assistedData`: see section 6.

            ## 6. assistedData (used by both coachInsights and missingSkills)
            This drives a short coaching interview in the UI. The tone is friendly and conversational, written to the candidate in the second person.
            - `initialPrompt`: one friendly question that asks the candidate what they actually did, e.g. "Love this AI initiative! Could you tell me a bit about what this application actually did and what parts you personally put together?"
            - `subtext`: one sentence on why candidates under-describe this kind of work.
            - `equivalentTools`: for missing skills, tools the candidate may have used that count as equivalent. Empty list otherwise.
            - `chips`: 3-4 realistic answers to the question. Each has a short `label` (a first-person accomplishment, e.g. "Built the analytics dashboard UI"), `details` (one line) and an optional `roleHint`. Always include one final chip with `isNegative: true` such as "Haven't worked with this yet".
            - `drillDownQuestion`: a follow-up question about scope, scale or impact. `drillDownChips`: 3-4 answer chips for it.
            - `realityCheck`:
            - `jdExpectation`: what the JD actually expects.
            - `candidateReality`: what the resume currently shows, honestly.
            - `coachAdvice`: one line of straight advice, including whether the candidate should avoid claiming it.
            - `authenticDrafts`: 2-3 drafts, each with `title`, `text` and `tags`. Each must be truthful if the candidate picks the matching chips, and must use [placeholders] for unknown specifics.
            - `placementOptions`: 1-3 places the text could go. Each has `label`, `section` ("experience", "projects", "skills" or "custom"), `roleName` (the exact role/company/project name from the resume) and `reason`. Mark the best one `isRecommended: true` and set `suggestedPlacementId` to its id.

            ## Final check before responding
            - Every `bulletId` and `targetLine` exists in resumeData (or targetLine is 0).
            - The three counts add up to the total number of requirements.
            - No invented facts, and placeholders are used wherever data is unknown.
            - Output is valid JSON matching the schema, with nothing else.
        """,
    input_variables=['structured_jd_content','structured_resume','role','company']
)
# End Of Prompt

# 2. Define the service function
def compare_jd_resume(structured_jd_content: dict[str, Any] | None,structured_resume:dict[str, Any] | None,role:str,company:str):
    """Uses LangChain with Structured Outputs to extract JSON from resume text."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,  # Gemini 3.0+ defaults to 1.0
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
        )
    
    # Enforces the Pydantic schema on the model output
    structured_resp = llm.with_structured_output(FitLensAnalysisData)
    # Create a single runnable chain
    chain = matchPrompt | structured_resp
    # Invoke the chain with your variables
    result = chain.invoke({'structured_jd_content':structured_jd_content,'structured_resume':structured_resume,'role':role,'company':company})
    if isinstance(result, FitLensAnalysisData):
            return result
    else:
        raise ValueError("LLM response did not match ResumeData structure.")