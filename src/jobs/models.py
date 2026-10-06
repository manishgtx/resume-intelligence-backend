from sqlalchemy import DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional, Any
from src.jobs.dtos import JobStatus
from src.utils.db import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    user_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    title:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=False)
    company:Mapped[str] = mapped_column(nullable=False)
    result: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    match_result: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    errorMessage: Mapped[str] = mapped_column(nullable=True)
        
    status: Mapped[JobStatus] = mapped_column(default=JobStatus.PROCESSING, nullable=False)
    is_verified:Mapped[bool] = mapped_column(default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    verified_at:Mapped[datetime] = mapped_column(DateTime,nullable=True)