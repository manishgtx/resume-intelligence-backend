# from pydantic import BaseModel, Field

from pydantic import BaseModel, Field


class candidateEvaluation(BaseModel):
    reasoning: str = Field(
        description="Brief explanation of why the candidate passed/failed eligibility and earned this score."
    )
    basic_eligibility: bool = Field(
        description="True if all hard criteria are met, False otherwise."
    )
    score: int = Field(
        description="Match score from 1 to 100 based on fit.", ge=1, le=100
    )

# class candidateEvaluation(BaseModel):
#     basicEligibility: bool = Field(
#         description=(
#             "Set to True ONLY if the candidate meets all non-negotiable hard criteria "
#             "specified in the job description (e.g., minimum required years of experience, "
#             "required degrees, must-have core technologies, or mandatory certifications). "
#             "Set to False if any absolute dealbreaker is failed."
#         )
#     )
    # score: int = Field(
    #     ge=1,
    #     le=100,
    #     description=(
    #         "An overall match score from 1 to 100 based on skill overlap, relevant experience, "
    #         "domain knowledge, and role alignment. "
    #         "1-40: Low match / unqualified, "
    #         "41-69: Partial match / missing key requirements, "
    #         "70-85: Strong candidate, "
    #         "86-100: Exceptional / ideal fit."
    #     ),
    # )
    # reasoning: str = Field(
    #     description=(
    #         "A concise 2-3 sentence justification explaining the score and basic eligibility determination, "
    #         "highlighting key strengths or missing requirements."
    #     )
    # )