from ...state import CareerState
from langchain_groq import ChatGroq
import pypdf
from langchain_core.documents import Document
from .schema import evaluation
from .prompt import basicEligibility

def candidateEvaluation(state:CareerState) -> CareerState:
    # resume_content = state['resume_content']
    # job_description = state['job_description']
    
    # llm = ChatGroq(
    #     model="llama-3.3-70b-versatile",
    #     temperature=0,
    #     max_tokens=None,
    #     timeout=None,
    #     max_retries=2,
    #     # other params...
    # )
    # structured_resp = llm.with_structured_output(evaluation)
    # print(structured_resp.invoke(basicEligibility.invoke({'resume_content':resume_content,'job_description':job_description})))
    return state