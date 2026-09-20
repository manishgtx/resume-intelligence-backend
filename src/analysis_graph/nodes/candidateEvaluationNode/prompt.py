from langchain_core.prompts import PromptTemplate
basicEligibility = PromptTemplate(
    template= """
        You are evaluating a candidate's resume against job description criteria.
        Inputs:

        List of JD Criteria (with IDs): {structuredJD}

        Structured Resume Lines (with IDs): {structuredResume}

        Analyze the candidate resume against the target job description and return the structured FitLens analysis."
        """,
    input_variables=['structuredJD','structuredResume']
)


