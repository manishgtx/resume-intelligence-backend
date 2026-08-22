from langchain_core.prompts import PromptTemplate
jdTemplate = PromptTemplate(
    template= """
            # Role
            You are an expert HR Data Extraction Specialist. Your sole task is to analyze the provided Job Description (JD) text and extract all explicit requirements, operational details, and candidate criteria into the requested target schema.
    
            ---
    
            ## Strict Rules & Extraction Directives
    
            ### 1. Zero Hallucination & Strict Fidelity
            - Extract ONLY information that is explicitly stated or directly implied by the JD text.
            - Do NOT infer standard industry qualifications if they are not written (e.g., do not assume a Bachelor's degree is required unless stated).
            - If a field or category is missing from the JD, leave it empty or `null` as permitted by the schema.
    
            ### 2. Disambiguation: Mandatory vs. Preferred
            - **Mandatory Requirements**: Items prefixed with "Required", "Must have", "Essential", "Minimum", "Basic Qualifications", or written as non-negotiable prerequisites.
            - **Preferred Qualifications**: Items prefixed with "Preferred", "Nice to have", "Bonus points for", "Plus", "Desired", or "Ideal candidate".
            - If a skill is listed without a clear distinction, classify it as **Mandatory**.
    
            ### 3. Numerical & Standardization Rules
            - **Years of Experience**: Extract the exact lower-bound numeric integer where possible (e.g., "5+ years" -> `5`, "3 to 5 years" -> `3`). If a range is given, capture the minimum required years.
            - **Skills**: Atomize skill lists. Extract individual skills/tools as separate array items (e.g., split "Python/Django/PostgreSQL" into `["Python", "Django", "PostgreSQL"]`).
            - **Education**: Standardize degree levels into high-level categories (e.g., "Bachelor's", "Master's", "PhD", "High School / Associate") while capturing specific major preferences in the description/field provided.
    
            ### 4. Operational Context
            - **Work Model**: Classify accurately into `On-site`, `Remote`, or `Hybrid`. If not specified, default to `Unspecified`.
            - **Employment Type**: Classify into `Full-time`, `Part-time`, `Contract`, `Internship`, or `Temporary`.
    
            ---
    
            ## Input Job Description
            {jobDescription}
        """,
    input_variables=['jobDescription']
)

