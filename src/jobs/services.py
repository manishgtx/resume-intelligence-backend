from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from .dtos import StructuredJD
load_dotenv()

# Start Of Prompt
from langchain_core.prompts import PromptTemplate
jdPrompt = PromptTemplate(
    template= """
            You are a job description analyst. Extract structured information from the job description provided by the user. Output ONLY valid JSON with exactly these four keys: mustHaves, keyDeliverables, buriedSignals, missingSkills. No markdown, no commentary.

            RULES
            1. Use ONLY information present in the JD. Never invent requirements.
            2. If a section has no content, return [].

            mustHaves
            - Hard requirements: phrases like "required", "must", "X+ years", "strong experience in", or items under a "Requirements" or "Qualifications" heading.
            - Exclude anything marked "nice to have", "preferred", "bonus", or "plus".
            - Max 8 items, ordered by importance.
            - Fields: id (mh_1, mh_2...), title, subtitle, category ("must-have"), keywords, minYears, evidence.
            - minYears only if the JD states a number, otherwise null.
            - keywords: 2-5 normalized terms, e.g. ["TypeScript", "production"].
            - evidence: exact sentence or fragment from the JD.

            keyDeliverables
            - What the person will build, ship, or own (from "Responsibilities" or "What you'll do").
            - Max 6 items.
            - Fields: id (kd_1, kd_2...), title, subtitle, category ("key-deliverable"), keywords, evidence.

            buriedSignals
            - Implicit expectations not stated as formal requirements: ownership, speed, ambiguity, scale, collaboration style, leadership, culture cues.
            - Max 5. Each must be backed by an exact JD phrase in evidence.
            - Fields: id (bs_1, bs_2...), signal, evidence, resumeHint.
            - resumeHint: one short line on what resume evidence would prove it.

            missingSkills
            - Every distinct tool, technology, practice, or experience area the JD mentions or clearly implies, including those in nice-to-haves and must-haves.
            - Fields: name, type, mentions, inMustHave.
            - name: normalized (group synonyms, e.g. "k8s" and "Kubernetes" become "Docker / Kubernetes" if the JD pairs them, otherwise one name).
            - type: "skill" for tools/technologies, "experience" for practices/exposure (e.g. CI/CD, performance monitoring, scale).
            - mentions: count of occurrences including synonyms, minimum 1.
            - inMustHave: true if it appears in a must-have.

            GENERAL
            - Titles are short and plain, with no filler.
            - Do not output status or statusLabel.

            ---
    
            ## Input Resume
            {jd_content}
        """,
    input_variables=['jd_content']
)
# End Of Prompt

# 2. Define the service function
def extract_jd_data(raw_text: str):
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
    structured_resp = llm.with_structured_output(StructuredJD)
    # Create a single runnable chain
    chain = jdPrompt | structured_resp
    # Invoke the chain with your variables
    result = chain.invoke({'jd_content': raw_text})
    if isinstance(result, StructuredJD):
            return result
    else:
        raise ValueError("LLM response did not match ResumeData structure.")