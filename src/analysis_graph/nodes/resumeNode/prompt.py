from langchain_core.prompts import PromptTemplate
resumePrompt = PromptTemplate(
    template= """
            Parse the provided resume into standard sections. Within each section, break content down into individual lines or bullet points. Assign each line a unique sequential ID starting with 'line_1'. Preserve the original wording.
    
            ## Input Resume
            {resume_content}
        """,
    input_variables=['resume_content']
)

