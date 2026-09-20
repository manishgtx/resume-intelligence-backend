from pydantic import BaseModel
from typing import Any, Dict, Optional

class ResumeStatusResponse(BaseModel):
    id: int
    status: str
    extracted_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True