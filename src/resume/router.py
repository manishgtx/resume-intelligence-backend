from datetime import datetime, timezone
from fastapi import APIRouter, File,UploadFile,BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.resume.dtos import ResumeStatusResponse, ResumeData
from src.resume import controller,data
from src.utils.db import get_db
from src.utils.errors import DatabaseError, Missing

resume_router = APIRouter(tags=["Resume"])

@resume_router.post("/resumes/extract", status_code=202)
def extract_resume(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    return controller.extract_resume(file,background_tasks,db)

# The Web layer endpoint function should be the only place that catches these exceptions and translates them into `HTTPException` responses with status codes
# Get Specfic Resume
@resume_router.get("/resumes/{resume_id}", response_model=ResumeStatusResponse)
def get_resume_status(resume_id: int, db: Session = Depends(get_db)):
    try:
        return data.get_resume_by_id(resume_id,db)
    except Missing as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.msg
        )
    except DatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.msg
        )


# @resume_router.post("/resume")
# def upload_resume(resume: UploadFile = File(...,description="Upload Resume PDF"),db: Session = Depends(get_db)):
#     return controller.upload_resume(resume,db)

@resume_router.patch("/resumes/{resume_id}/verify")
def verify_resume(
    resume_id: int,
    update_data: ResumeData,
    db: Session = Depends(get_db)
):
    try:
        return controller.verify_resume(resume_id,update_data,db)
    except Missing as exc:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=exc.msg
            )
    except DatabaseError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.msg
        )
    