from sqlalchemy import Column, Integer, String, Float, DateTime
from src.utils.db import Base
from datetime import datetime
class ResumeAnalysis(Base):
    __tableName__: 'resume_analysis'
    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, nullable=False)
    job_id = Column(Integer, nullable=False)
    match_score = Column(Float, nullable=True)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
