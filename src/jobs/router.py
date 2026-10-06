from fastapi import APIRouter, BackgroundTasks,Depends
from src.jobs import controller
from src.jobs.dtos import JobDescription
from src.utils.db import get_db
from sqlalchemy.orm import Session

jobs_router = APIRouter(prefix="/jobs",tags=["Jobs"])

@jobs_router.post('/descriptions')
def upload_job_descriptions(
    body: JobDescription,
    background_tasks: BackgroundTasks = BackgroundTasks(),
    db: Session = Depends(get_db)):
    return controller.upload_job_descriptions(body,background_tasks,db)

@jobs_router.post('/check')
def testing():
    return controller.testing()
    