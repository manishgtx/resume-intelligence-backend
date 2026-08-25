from fastapi import UploadFile, HTTPException
from pypdf import PdfReader
import io
from sqlalchemy.orm import Session
from src.resume.models import Resume

def upload_resume(resume: UploadFile,db:Session):

    # 1) Checking content type is PDF or not.
    if resume.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    # 2) check for file size (File Size < 500KB)
    file_data = resume.file.read()

    if len(file_data) > 500 * 1024:
        raise HTTPException(
            status_code=400,
            detail="Resume size cannot exceed 500 KB"
        )

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
    resume_record = Resume(
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