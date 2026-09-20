from fastapi import APIRouter, Depends
from src.analysis import controller
from src.analysis.dtos import ResumeAnalysisCreate
from src.utils.db import get_db
from sqlalchemy.orm import Session

analysis_router = APIRouter(tags=["Analysis"])

@analysis_router.get("/resume-analysis")
def resume_analysis(db: Session = Depends(get_db)):
    return controller.resume_analysis(db)

@analysis_router.get("/jobs/criticality")
def get_job_desc(jd:str):
    return controller.get_job_desc(jd)
