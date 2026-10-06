from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .dtos import ResumeData
load_dotenv()

# Start Of Prompt
from langchain_core.prompts import PromptTemplate
resumePrompt = PromptTemplate(
    template= """
            You are an expert resume parsing engine. Your task is to extract structured information from the provided resume text and map it accurately into the target JSON schema.

            ### Guidelines & Rules:

            1. **Fidelity to Source (No Hallucination):**
            - Extract only information explicitly stated in the text.
            - Do not infer, assume, or fabricate any dates, contact info, job titles, or metrics.
            - If an optional field is missing from the source text, set it to `null` (or an empty array `[]` for list fields).

            2. **Identifiers (`id` fields):**
            - The schema requires an `id` string for items in education, experience, projects, certifications, etc.
            - Generate clean, sequential identifiers prefixed by section type:
                - Education: `"edu-1"`, `"edu-2"`
                - Work Experience: `"exp-1"`, `"exp-2"`
                - Projects: `"proj-1"`, `"proj-2"`
                - Internships: `"intern-1"`, `"intern-2"`
                - Certifications: `"cert-1"`, `"cert-2"`
                - Extra-Curricular: `"extra-1"`, `"extra-2"`
                - Leadership: `"lead-1"`, `"lead-2"`
                - Custom Sections: `"custom-1"`, `"custom-2"`

            3. **Work Experience Bullets:**
            - Every bullet in `workExperience[].bullets` must be represented as an object: `{{"text": "<bullet text>", "isInteractive": false}}`.
            - Maintain the original meaning and specific metrics verbatim; do not rephrase unless fixing broken line breaks or raw PDF extraction artifacts.

            4. **Skills Categorization:**
            - If technical skills are explicitly separated into categories (e.g., Languages, Frameworks/Libraries, Tools), populate `languages`, `libraries`, and `tools` accordingly.
            - For all other domain-specific skill groupings, populate the `categories` list using the `SkillCategory` structure.

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