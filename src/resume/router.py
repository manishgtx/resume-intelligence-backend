from fastapi import APIRouter, File,UploadFile,BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.resume.dtos import ResumeStatusResponse
from src.resume import controller
from src.utils.db import get_db

resume_router = APIRouter(tags=["Resume"])

@resume_router.post("/resumes/extract", status_code=202)
def extract_resume(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)
):
    return controller.extract_resume(file,background_tasks,db)


# Get Specfic Resume
@resume_router.get("/resumes/{resume_id}", response_model=ResumeStatusResponse)
def get_resume_status(resume_id: int, db: Session = Depends(get_db)):
    print(resume_id,'checking')
    resume = controller.get_resume_by_id(resume_id,db)
    # If the resume ID doesn't exist, return a 404
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with ID {resume_id} not found."
        )
    return resume
        
# @resume_router.get("/testing",response_model=ResumeData)
# def extract_res(db: Session = Depends(get_db)):
#     query = db.query(ResumeRecord).filter(ResumeRecord.id == 2).first()
#     if query is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Resume not found"
#         )
#     raw_text = query.raw_text
#     if raw_text is None:
#         raise HTTPException(
#             status_code=404,
#             detail="Resume text is not available"
#         )
#     result = extract_resume_data(raw_text)
#     return result


# @resume_router.post("/resume")
# def upload_resume(resume: UploadFile = File(...,description="Upload Resume PDF"),db: Session = Depends(get_db)):
#     return controller.upload_resume(resume,db)