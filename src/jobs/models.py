from sqlalchemy import Column, Integer, Text, DateTime
from src.utils.db import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)