from ...state import CareerState
from langchain_groq import ChatGroq
from .schema import ResumeExtractionOutput
from langchain_google_genai import ChatGoogleGenerativeAI
from .prompt import resumePrompt

def resumeIngestion(state:CareerState) -> CareerState:
    resume_content = state['resume_content']
    llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
    )
    structured_resp = llm.with_structured_output(ResumeExtractionOutput)
    structured_resume_resp = structured_resp.invoke(resumePrompt.invoke({'resume_content':resume_content}))
    return {'structuredResume':structured_resume_resp}
    # return state