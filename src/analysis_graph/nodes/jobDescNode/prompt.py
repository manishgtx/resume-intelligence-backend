from langchain_core.prompts import PromptTemplate
jdTemplate = PromptTemplate(
    template= """
            You are an expert technical recruiter analyzing a Job Description to build an automated screening benchmark.

            Your task:
            1. Extract all discrete requirements from the text.
            2. Break compound or bundled requirements into separate, atomic criteria (e.g., "Experience with React and Node.js" must become two separate entries).
            3. Assign a unique sequential ID starting with "crit_1".
            4. Categorize each criterion into one of three priority tiers:
            - "must_have": Explicitly stated as required, minimum qualifications, core responsibilities, or non-negotiable prerequisites.
            - "nice_to_have": Stated as desired, preferred, or "good to have".
            - "bonus_preferred": Explicitly mentioned as a "plus", "bonus points", or specialized edge-case skills that set top candidates apart.

            Ensure no implicit or subtle requirements are overlooked, and keep each requirement statement concise and verifiable.

            Extract requirements from this job description:
            {jobDescription}
        """,
    input_variables=['jobDescription']
)

