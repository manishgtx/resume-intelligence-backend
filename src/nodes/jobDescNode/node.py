from src.state import CareerState
from langchain_groq import ChatGroq
from .schema import JobDescriptionData
from .prompt import jdTemplate

def jobDescriptionIngestion(state:CareerState) -> CareerState:
    jobDescription = state['job_description']
    llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
    # structured_resp = llm.with_structured_output(JobDescriptionData)
    # structuredJD = structured_resp.invoke(jdTemplate.invoke({'jobDescription':jobDescription}))
    # return {'structured_jd':structuredJD}
    return state