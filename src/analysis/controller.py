from src.analysis.dtos import ResumeAnalysisCreate
from sqlalchemy.orm import Session
from src.resume.controller import get_resume_by_id
from src.jobs.controller import get_job_by_id
from src.analysis_graph import workflow

def resume_analysis(body:ResumeAnalysisCreate,db:Session):
    resume = get_resume_by_id(body.resume_id,db)
    job = get_job_by_id(body.job_id,db)
    print(job.description)
    print(resume.extracted_text)
    ai_msg=workflow.invoke({"jobDescription":job.description})
    # print(ai_msg)
    return {"message":ai_msg}