from ...state import CareerState
from langchain_groq import ChatGroq
from .schema import StructuredJD
from .prompt import jdTemplate
from typing import Any
from dotenv import load_dotenv
load_dotenv()

def jobDescriptionIngestion(state:CareerState) -> dict[str, Any]:
    jobDescription = state['jobDescription']
    llm = ChatGroq(
            model="openai/gpt-oss-120b",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )
    structured_resp = llm.with_structured_output(StructuredJD)
    structuredJD_resp = structured_resp.invoke(jdTemplate.invoke({'jobDescription':jobDescription}))
    return {'structuredJD':structuredJD_resp}
    # return state