from sqlalchemy import Column, Integer, String, DateTime, LargeBinary, Text
from src.utils.db import Base
from datetime import datetime

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_data = Column(LargeBinary)
    extracted_text = Column(Text)
    created_at = Column(DateTime, default=datetime.now)