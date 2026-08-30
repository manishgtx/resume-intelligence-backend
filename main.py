from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.db import Base, engine
# Routers
from src.resume.router import resume_router
from src.jobs.router import jobs_router
from src.analysis.router import analysis_router

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization note: {e}")

app = FastAPI(
    title="Resume Application API",
    description="API for validating and processing resumes and job descriptions with separate dedicated endpoints",
    version="2.0.0"
)

app.include_router(resume_router)
app.include_router(jobs_router)
app.include_router(analysis_router)

# Enable CORS for cross-origin requests from frontend apps (e.g., Angular, React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {
        "message": "Resume & Job Application API is running.",
        "endpoints": {
            "upload_resume": "POST /resume (or POST /resume)",
            "job_description": "POST /job/description (or POST /job)",
        }
    }