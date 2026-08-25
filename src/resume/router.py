from fastapi import APIRouter, File,UploadFile,Depends
from src.resume import controller
from src.utils.db import get_db
from sqlalchemy.orm import Session

resume_router = APIRouter(tags=["Resume"])

@resume_router.post("/resume")
def upload_resume(resume: UploadFile = File(...,description="Upload Resume PDF"),db: Session = Depends(get_db)):
    return controller.upload_resume(resume,db)