from pydantic import BaseModel

class ResumeAnalysisCreate(BaseModel):
    resume_id: int
    job_id: int
    