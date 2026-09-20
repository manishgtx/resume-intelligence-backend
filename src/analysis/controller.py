from src.analysis.dtos import ResumeAnalysisCreate
from sqlalchemy.orm import Session
from src.resume.controller import get_resume_by_id
from src.jobs.controller import get_job_by_id
from src.analysis_graph import workflow

jobdata = """
    **At Airbus, we are harnessing the power of artificial intelligence to enhance efficiency and quality across our value chain. Our team is composed of technologists and business leaders dedicated to innovation and excellence.**

**We are seeking a visionary, highly skilled, and innovative AI Engineer (4–7 Years) to join our high-impact team. In this role, you will architect, build, and deploy production-grade AI-driven products designed to automate complex engineering workflows, accelerate software transformation, and drive intelligent digital paradigms. You will turn ambiguous, cutting-edge AI concepts into scalable, reliable, cost effective and high-performing enterprise platforms.**

**Qualification & Experience:**

**Education: Bachelor’s or Master’s degree in Computer Science, Artificial Intelligence, Data Science, Software Engineering, or a related quantitative field.**

**Required Certification: Must hold at least one recognized cloud or AI certification (e.g., Google Cloud Professional Machine Learning Engineer or equivalent advanced AI/Cloud credentials).**

**Experience: 4 to 7 years of hands-on experience in building, deploying, and scaling end-to-end AI/ML products, generative AI applications, code transformation tools, and intelligent software automation systems.**

**Key Responsibilities**

**End-to-End AI Product Engineering: Lead the lifecycle of advanced AI products—from architectural design and model selection/fine-tuning to production deployment, monitoring, and performance optimization.**

**Intelligent Automation & Modernization Solutions: Design and implement intelligent systems that parse, translate, and modernize complex legacy codebases and technical documentation using state-of-the-art Natural Language Processing (NLP) and Large Language Models (LLMs).**

**Prompt Engineering & Model Fine-Tuning: Develop robust prompt architectures, retrieval-augmented generation (RAG) pipelines, and fine-tuned models to automate domain-specific artifact generation and technical decision-making from high-level user prompts.**

**Cloud Architecture & Scalability: Leverage Google Cloud Platform (GCP) infrastructure to build resilient, serverless, and scalable AI microservices and batch processing pipelines.**

**Cross-Functional Collaboration: Partner closely with Product Managers, UX Designers, Software Architects, and Domain Experts to ensure technical feasibility, clear system requirements, and frictionless integration into enterprise ecosystems.**

**Code Quality & Best Practices: Maintain high engineering standards by establishing CI/CD pipelines for AI assets, automated testing frameworks, robust API design, and comprehensive technical documentation.**

**Advocacy & Mentorship: Drive an innovation-first culture across the engineering lab, staying ahead of emerging Generative AI/ML research and mentoring junior team members on production ML engineering best practices.**

**Cloud Infrastructure & AI FinOps: Architect resilient, serverless, and scalable AI microservices on Google Cloud Platform (GCP) while implementing granular tagging, billing telemetry, and cost-attribution frameworks for all AI workloads.**

**Cost Tracking & Optimization: Monitor, analyze, and optimize model inference costs (token-based API spend, vector database queries, GPU/TPU utilization) to maintain full visibility into product operational costs.**

### **Technical Essentials**

- **Cloud Platform Mastery: Extensive expertise in Google Cloud Platform (GCP), including Vertex AI, Cloud Run, BigQuery, Cloud Functions, and GKE.**
- **Generative AI & LLM Frameworks: Strong proficiency in applying LLMs, RAG architectures, vector databases (e.g., Pinecone, ChromaDB, Vertex Vector Search), and frameworks like LangChain or LlamaIndex to build complex software automation tools.**
- **Programming & Software Engineering: Mastery of Python and solid proficiency in modern web/backend stacks (RESTful APIs, gRPC, microservice design patterns, modern frontend frameworks).**
- **Code Parsing & AST Analysis: Familiarity with abstract syntax trees (ASTs), static code analysis, compiler concepts, or domain-specific language (DSL) translation techniques.**
- **MLOps & DevOps: Hands-on experience with MLOps workflows, model tracking, automated testing, containerization (Docker, Kubernetes), and CI/CD pipelines.**
- **AI Cost Monitoring & FinOps: Proven experience in token metering, cost attribution, model routing policies (balancing frontier models vs. smaller open-source models for cost efficiency), and monitoring tools (OpenTelemetry, Cloud Monitoring).**

### **Soft Skills & Behavioral Attributes**

- **Strategic Product Mindset: Ability to translate complex client or internal business requirements into practical, scalable AI features with measurable ROI.**
- **Articulate Communication: Exceptional verbal and written communication skills with a proven ability to explain complex AI/ML mechanics to non-technical business leaders and senior technical stakeholders alike.**
- **Innovative & Creative Problem-Solver: Thrives in an ambiguous, lab-oriented environment where novel user experience and software engineering paradigms must be invented from scratch.**
- **High Empathy & User Advocacy: Deep passion for understanding engineering pain points and translating legacy technical debt into streamlined digital products.**

## **Nice-to-Have / Added Advantages**

- **Prior experience building source-to-source compilers, automated code conversion utilities, or automated design document generators.**
- **Familiarity with software architecture patterns, legacy enterprise frameworks, and multi-language code conversion strategies.**
- **Knowledge of quantitative product analytics to track AI feature adoption, model accuracy, and user efficiency improvements.**
- **An active GitHub profile or portfolio demonstrating end-to-end AI applications, open-source contributions, or custom LLM tooling.**

## **Success Metrics**

- **Product Efficiency & Impact: Quantifiable reduction in manual technical debt and turnaround time for automated code and document generation tasks.**
- **System Scalability & Reliability: High uptime, low inference latency, and robust error handling across production AI pipelines on GCP.**
- **Innovation & Quality: Successful deployment of high-accuracy AI models that consistently outperform baseline metrics in complex, domain-specific tasks.**
- **Collaboration & Delivery Efficiency: Timely feature releases, clean API handoffs, low rework rates, and strong cross-functional alignment throughout the product lifecycle.**

This job requires an awareness of any potential compliance risks and a commitment to act with integrity, as the foundation for the Company’s success, reputation and sustainable growth."""

def resume_analysis(db):
    # resume = get_resume_by_id(body.resume_id,db)
    resume = get_resume_by_id(6,db)
    # job = get_job_by_id(body.job_id,db)
    
    # print(job.description)
    # print(resume.extracted_text)
    ai_msg=workflow.invoke({"resume_content":resume.extracted_text,"jobDescription":jobdata})
    print(ai_msg)
    return ai_msg['evaluation']

def get_job_desc(jd:str):
    ai_msg=workflow.invoke({"jobDescription": jd})
    
    print(type(ai_msg))
    return ai_msg