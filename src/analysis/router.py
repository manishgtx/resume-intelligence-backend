from fastapi import APIRouter, Depends
from src.analysis import controller
from src.analysis.dtos import ResumeAnalysisCreate
from src.utils.db import get_db
from sqlalchemy.orm import Session

analysis_router = APIRouter(tags=["Analysis"])

@analysis_router.post("/resume-analysis")
def resume_analysis(body: ResumeAnalysisCreate,db: Session = Depends(get_db)):
    return controller.resume_analysis(body,db)
