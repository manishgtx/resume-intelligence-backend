from ...state import CareerState
from .schema import EvaluationOutput
from .prompt import basicEligibility
from langchain_google_genai import ChatGoogleGenerativeAI

def candidateEvaluation(state:CareerState) -> CareerState:
    structuredResume = state['structuredResume']
    structuredJD = state['structuredJD']
    
    llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.0,  # Gemini 3.0+ defaults to 1.0
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
    )
    structured_resp = llm.with_structured_output(EvaluationOutput,method="json_mode")
    evaluation = structured_resp.invoke(basicEligibility.invoke({'structuredResume':structuredResume,'structuredJD':structuredJD}))
    return {"evaluation":evaluation}