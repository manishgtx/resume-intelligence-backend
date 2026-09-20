from ...state import CareerState
# from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from .schema import JobDescriptionExtraction
from .prompt import jdTemplate
from typing import Any
from dotenv import load_dotenv
load_dotenv()

def jobDescriptionIngestion(state:CareerState) -> dict[str, Any]:
    jobDescription = state['jobDescription']
    llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=1.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
    )
    structured_resp = llm.with_structured_output(JobDescriptionExtraction)
    structuredJD_resp = structured_resp.invoke(jdTemplate.invoke({'jobDescription':jobDescription}))
    print(structuredJD_resp)
    return {'structuredJD':structuredJD_resp}