from fastapi import APIRouter,Depends
from src.jobs import controller
from src.jobs.dtos import JobDescription
from src.utils.db import get_db
from sqlalchemy.orm import Session

jobs_router = APIRouter(prefix="/jobs",tags=["Jobs"])

@jobs_router.post('/descriptions')
def upload_job_descriptions(body: JobDescription,db: Session = Depends(get_db)):
    return controller.upload_job_descriptions(body,db)