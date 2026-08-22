from src.state import CareerState
from langchain_groq import ChatGroq
import pypdf
from langchain_core.documents import Document
from .schema import StructuredResume
# from .prompt import jdTemplate

def resumeIngestion(state:CareerState) -> CareerState:
    reader = pypdf.PdfReader(state['resume_path'])
    resume_content =[
        Document(
            page_content=page.extract_text() or "",
            metadata={"source": state['resume_path'], "page": i},
        )
        for i, page in enumerate(reader.pages)
    ]
    full_resume_text = "\n".join(doc.page_content for doc in resume_content)
    # llm = ChatGroq(
    #     model="llama-3.1-8b-instant",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     # other params...
    # )
    # structured_resp = llm.with_structured_output(StructuredResume)
    return {'resume_content':full_resume_text}