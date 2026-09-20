from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column
from src.utils.db import Base
from datetime import datetime
from typing import Optional, Any

class ResumeRecord(Base):
    __tablename__ = "resume_records"

    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    user_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    raw_text:Mapped[Optional[str]] = mapped_column(nullable=True)
    extracted_data: Mapped[Optional[dict[str, Any]]] = mapped_column(JSON, nullable=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # ⚙️ Status Pipeline: "processing" ➔ "draft" (or "failed") ➔ "verified"
    status: Mapped[str] = mapped_column(String(50), default="processing", nullable=False)
    is_verified:Mapped[bool] = mapped_column(default=False, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    verified_at:Mapped[datetime] = mapped_column(DateTime,nullable=True)