from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .dtos import ResumeData
load_dotenv()

# Start Of Prompt
from langchain_core.prompts import PromptTemplate
resumePrompt = PromptTemplate(
    template= """
            You are an expert resume parsing engine.
            Your task is to parse the candidate's raw resume text into the provided structured schema with extreme fidelity.
            Extraction Rules:
            1. Split paragraph blocks under work experience and projects into distinct, crisp, standalone bullet points.
            2. Preserve original numbers, percentages, metrics, and technical keywords exactly as stated.
            3. Categorize skills appropriately into languages, libraries/frameworks, and tools.
            4. If a field is not present in the resume text, set it to null or an empty list. Never invent or hallucinate information.
            ---
    
            ## Input Resume
            {resume_content}
        """,
    input_variables=['resume_content']
)
# End Of Prompt

# 2. Define the service function
def extract_resume_data(raw_text: str):
    """Uses LangChain with Structured Outputs to extract JSON from resume text."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0,  # Gemini 3.0+ defaults to 1.0
        max_tokens=None,
        timeout=None,
        max_retries=2,
        # other params...
        )
    
    # Enforces the Pydantic schema on the model output
    structured_resp = llm.with_structured_output(ResumeData)
    # Create a single runnable chain
    chain = resumePrompt | structured_resp
    # Invoke the chain with your variables
    result = chain.invoke({'resume_content': raw_text})
    if isinstance(result, ResumeData):
            print(type(result))
            return result
    else:
        raise ValueError("LLM response did not match ResumeData structure.")