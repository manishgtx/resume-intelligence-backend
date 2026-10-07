from typing import cast
from fastapi import UploadFile, HTTPException, BackgroundTasks
from pypdf import PdfReader
import io,os
from sqlalchemy.orm import Session
from src.resume.models import ResumeRecord
from .services import extract_resume_data
from src.resume import data


from src.utils.db import LocalSession

# PDF Extraction
def extract_text_from_pdf(file_path: str) -> str:
    """Synchronous CPU-bound function to extract text using pypdf."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text



def upload_resume(resume: UploadFile,db:Session):

    # 1) Checking content type is PDF or not.
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # 2) check for file size (File Size < 500KB)
    file_data = resume.file.read()

    # if len(file_data) > 500 * 1024:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Resume size cannot exceed 500 KB"
    #     )

    # 3) Check for Number of Page (Pages < 6)
    pdf = PdfReader(io.BytesIO(file_data))
    
    if len(pdf.pages) > 5:
        raise HTTPException(
            status_code=400,
            detail="Resume cannot have more than 5 pages"
        )

    # 4) Text extraction
    text = ""
    for page in pdf.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Could not extract text from the PDF"
        )

    # 5) Save resume in the database
    resume_record = ResumeRecord(
        file_name=resume.filename,
        file_data=file_data,
        extracted_text=text
    )
    
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)


    return {
        "id": resume_record.id,
        "filename": resume_record.file_name,
        "message": "Resume uploaded successfully"
    }


def extract_resume(
    file: UploadFile,
    background_tasks: BackgroundTasks,
    db: Session
):
    # 1. Create DB record synchronously (No await!)
    new_resume = ResumeRecord(status="processing", filename=file.filename)
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)
    
    resume_id: int = cast(int, new_resume.id)

    # 2. Save temporary local file
    file_path = f"/tmp/resume_{resume_id}.pdf"
    with open(file_path, "wb") as f:
        f.write(file.file.read())
        
    # 3. Add task to background execution
    background_tasks.add_task(process_resume, resume_id, file_path)

    # 4. Return instant 202 Accepted response 
    return {"message": "Processing started", "resume_id": resume_id}


def attach_ids(raw_resume_dict: dict) -> dict:
    """
    Attaches clean, deterministic IDs to all resume sections right after LLM extraction,
    before storing in the database or sending to the frontend.
    """
    # 1. Work Experience & Sequential Bullet IDs (1, 2, 3...)
    bullet_counter = 1
    for i, exp in enumerate(raw_resume_dict.get("workExperience") or []):
        exp["id"] = f"exp-{i + 1}"
        formatted_bullets = []
        for bullet in exp.get("bullets") or []:
            text = bullet if isinstance(bullet, str) else bullet.get("text", "")
            formatted_bullets.append({
                "id": bullet_counter,
                "text": text.strip(),
                "isInteractive": False  # Default False; Step 3 will toggle the weak ones!
            })
            bullet_counter += 1
        exp["bullets"] = formatted_bullets

    # 2. Education IDs (edu-1, edu-2...)
    for i, edu in enumerate(raw_resume_dict.get("education") or []):
        edu["id"] = f"edu-{i + 1}"

    # 3. Project IDs (proj-1, proj-2...)
    for i, proj in enumerate(raw_resume_dict.get("projects") or []):
        proj["id"] = f"proj-{i + 1}"

    # 4. Certification IDs (cert-1, cert-2...)
    for i, cert in enumerate(raw_resume_dict.get("certifications") or []):
        cert["id"] = f"cert-{i + 1}"

    # 5. Internship IDs (intern-1, intern-2...)
    for i, intern in enumerate(raw_resume_dict.get("internships") or []):
        intern["id"] = f"intern-{i + 1}"

    return raw_resume_dict


# background Task
def process_resume(resume_id: int, file_path: str):
    # 1. Create a fresh, independent session for the background task
    db = LocalSession() 
    try:
        # Extract PDF text and call OpenAI...
        text = extract_text_from_pdf(file_path)
        structured_text = extract_resume_data(text)
        
        # 2. Update DB with fresh session
        resume = db.query(ResumeRecord).filter_by(id=resume_id).first()
        if not resume:
            # Handling the None case satisfies the type checker
            print(f"Record with ID {resume_id} not found.")
            return
        
        resume.raw_text = text
        resume.status = "draft"
        resume.extracted_data = attach_ids(structured_text.model_dump())
        db.commit()
    except Exception as e:
        db.rollback()
        resume = db.query(ResumeRecord).filter_by(id=resume_id).first()
        if resume:
            resume.status = "failed"
            db.commit()
    finally:
        # 3. Always close the background session when done 
        db.close()
        # Clean up local file
        # Safe cleanup check 🧹
        if os.path.exists(file_path):
            os.remove(file_path)
        
    
# Questions
# Exception handling kaam kaise ka rahi hai hum yaha exception raise kar rahe hai. fir apne router me bhi hum dobara try catch laga rahe hai waha pe bhi inhe except kar rahe hai

def verify_resume(resume_id:int,update_data,db:Session):
    return data.verify_resume(resume_id,update_data,db)
        
def get_resume_status(resume_id:int,db:Session):
    return data.get_resume_by_id(resume_id,db)