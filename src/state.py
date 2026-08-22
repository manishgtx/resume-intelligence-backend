from typing import TypedDict

class CareerState(TypedDict):
    resume_path:str
    resume_content:str
    job_description:str
    structured_jd:str
    basic_eligibility:bool
    resume_score:int