from langchain_core.prompts import PromptTemplate
basicEligibility = PromptTemplate(
    template= """
        You are an expert technical recruiter evaluating a candidate's resume against a specific Job Description.

        ### TASK:
        Analyze the provided Resume against the Job Description and produce a structured evaluation.

        ### EVALUATION CRITERIA:
        1. **Basic Eligibility (`basicEligibility`)**:
        - Determine if the candidate meets ALL hard requirements (e.g., mandatory years of experience, required certifications, core required stack, legal/education requirements).
        - If ANY strict requirement is missing or unfulfilled, set `basicEligibility` to `false`. Otherwise, set it to `true`.

        2. **Match Score (`score`)**:
        - Assign a score between 1 and 100 representing how well the candidate fits the role overall.
        - Consider technical skills, depth of experience, relevance of past project impact, and alignment with responsibilities.

        ### INPUT DATA:

        --- BEGIN JOB DESCRIPTION ---
        {job_description}
        --- END JOB DESCRIPTION ---

        --- BEGIN RESUME ---
        {resume_content}
        --- END RESUME ---

        Evaluate the candidate now and output according to the requested JSON schema.
        """,
    input_variables=['jobDescription','resume_content']
)

