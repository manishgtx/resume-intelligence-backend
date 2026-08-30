from ...state import CareerState
from langchain_groq import ChatGroq
from .schema import StructuredResume
# from .prompt import jdTemplate

def resumeIngestion(state:CareerState) -> CareerState:
    # llm = ChatGroq(
    #     model="llama-3.1-8b-instant",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     # other params...
    # )
    # structured_resp = llm.with_structured_output(StructuredResume)
    # return {'resume_content':full_resume_text}
    return state