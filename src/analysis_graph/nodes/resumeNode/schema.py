from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class ResumeLine(BaseModel):
    id: str = Field(description="Unique ID for the line, e.g., 'line_1', 'line_2'")
    text: str = Field(description="The exact text of the bullet point, sentence, or line")

class ResumeSection(BaseModel):
    section_title: str = Field(description="Title of section, e.g., 'Work Experience', 'Education'")
    lines: List[ResumeLine]

class ResumeExtractionOutput(BaseModel):
    sections: List[ResumeSection]
    