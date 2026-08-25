from pydantic import BaseModel

class JobDescription(BaseModel):
    descriptions: list[str]