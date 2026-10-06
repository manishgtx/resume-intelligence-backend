from src.jobs.dtos import JobDescription, JobStatus, JobResponse
from sqlalchemy.orm import Session
from src.jobs.models import Job
from sqlalchemy.exc import SQLAlchemyError
from src.utils.errors import DatabaseError
import logging

logger = logging.getLogger(__name__)


def create_job(payload:JobDescription,db:Session) -> JobResponse:
    # doubtful about the errors how they will propogate, what about the model_validate what if error comes etc.
    # how logger is working
    try:
        job = Job(**payload.model_dump(),status=JobStatus.PROCESSING)
        db.add(job)
        db.commit()
        db.refresh(job)
        return JobResponse.model_validate(job)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error while creating job: {str(e)}")
        raise DatabaseError(msg="An internal database error occurred.")
        