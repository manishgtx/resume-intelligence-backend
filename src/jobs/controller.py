from sqlalchemy.orm import Session
from src.jobs.dtos import JobDescription
from src.jobs.models import Job
def upload_job_descriptions(body:JobDescription,db:Session):
    jobs = []
    for description in body.descriptions:
        job = Job(
            description=description
        )
        db.add(job)
        jobs.append(job)

    db.commit()
    return [
        {
            "id": job.id,
            "description": job.description
        }
        for job in jobs
        ]
    