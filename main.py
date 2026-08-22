from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.db import Base, engine

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Database initialization note: {e}")

app = FastAPI(
    title="Resume Application API",
    description="API for validating and processing resumes and job descriptions with separate dedicated endpoints",
    version="2.0.0"
)

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
            "upload_resume": "POST /resume/upload (or POST /resume)",
            "job_description": "POST /job/description (or POST /job)",
            "analyze_combined": "POST /resume/analyze"
        }
    }