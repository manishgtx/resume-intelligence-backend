from datetime import datetime, timezone
from src.resume.dtos import ResumeOut
from src.resume.models import ResumeRecord
from src.utils.errors import Missing, DatabaseError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging
from pydantic import ValidationError
logger = logging.getLogger(__name__)

def get_resume_by_id(resume_id:int,db:Session):
    # Get resume function can be used by most of the routes because we need to fetch resume in all of them.
    # (I think we should use it in all places) (how these exceptions will be handled isn't it make the things complicated)
    try:
        resume = db.query(ResumeRecord).filter_by(id=resume_id).first()
        if not resume:
            raise Missing(msg=f"Resume {resume_id} not found")
        return ResumeOut.model_validate(resume)
    
    except ValidationError as e:
        logger.error(f"Data mapping error for resume {resume_id}: {e}")
        # Raise an application error so the web layer knows something went wrong internally
        raise DatabaseError(msg="Data integrity error: record format is invalid.")
    
    except SQLAlchemyError as e:
        logger.exception(f"Database error while fetching resume {resume_id}: {e}")
        raise DatabaseError(msg="An internal database error occurred.")
    
def verify_resume(resume_id:int,update_data,db:Session):
    try:
        resume = db.query(ResumeRecord).filter_by(id=resume_id).first()
        if not resume:
            raise Missing(msg=f"Resume {resume_id} not found")
        
        resume.extracted_data = update_data.model_dump()
        
        # 3. Update status & metadata
        resume.status = "verified"
        resume.is_verified = True
        resume.verified_at = datetime.now(timezone.utc)
        
        # 4. Commit and refresh
        db.commit()
        db.refresh(resume)
        return ResumeOut.model_validate(resume)
    except ValidationError as e:
            logger.error(f"Data mapping error for resume {resume_id}: {e}")
            # Raise an application error so the web layer knows something went wrong internally
            raise DatabaseError(msg="Data integrity error: record format is invalid.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(f"Database error while fetching resume {resume_id}: {e}")
        raise DatabaseError(msg="An internal database error occurred.")