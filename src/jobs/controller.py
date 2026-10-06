from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from src.jobs.services2 import compare_jd_resume
from src.jobs.models import Job
from src.jobs.dtos import JobDescription, JobStatus
from src.jobs import data
from src.utils.db import LocalSession
from src.jobs.services import extract_jd_data
from src.resume import ResumeRecord

def upload_job_descriptions(
    payload: JobDescription,
    background_tasks: BackgroundTasks,
    db: Session
):
    job = data.create_job(payload,db)
        
    # 3. Add task to background execution
    background_tasks.add_task(process_job, job.id)

    # 4. Return instant 202 Accepted response 
    return {"message": "Processing started", "job_id": job.id}

def process_job(job_id: int):
    db = LocalSession()
    try:
        job_record = db.query(Job).filter_by(id=job_id).first()
        if job_record:
            job_record.status = JobStatus.PROCESSING
            db.commit()
            job_text = f"{job_record.title} {job_record.description} {job_record.company}"
            extracted_jd = extract_jd_data(job_text)
            job_record.result = extracted_jd.model_dump()
            db.commit()
            
        # Stage 2: compare with the user's resume (remove default user id after adding auth)
            resume = db.query(ResumeRecord).filter_by(id=14).first()
            if resume:
                structured_resume = resume.extracted_data
                structured_jd = job_record.result
                job_record.match_result = compare_jd_resume(structured_jd, structured_resume,job_record.company,job_record.title).model_dump()
                job_record.status = JobStatus.COMPLETED
                db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        job_record = db.query(Job).filter_by(id=job_id).first()
        if job_record:
            job_record.status = JobStatus.FAILED
            db.commit()
    finally:
            # 3. Always close the background session when done 
            db.close()
            
def testing():
    structured_jd = {
  "output": {
    "buried_signals": [
      {
        "evidence": "ability to work independently or as part of a collaborative team",
        "id": "bs_1",
        "resume_hint": "Examples of leading a feature or resolving a critical production issue solo.",
        "signal": "Expects independent problem solving"
      },
      {
        "evidence": "Write clean, well-documented, and efficient code and participate in code reviews",
        "id": "bs_2",
        "resume_hint": "Mentions of maintaining documentation or improving code review processes.",
        "signal": "High emphasis on code quality and documentation"
      },
      {
        "evidence": "requires an awareness of any potential compliance risks and a commitment to act with integrity",
        "id": "bs_3",
        "resume_hint": "Experience working in regulated industries or security-focused environments.",
        "signal": "Compliance-conscious engineering"
      }
    ],
    "key_deliverables": [
      {
        "category": "key-deliverable",
        "evidence": "Develop and maintain both front-end and back-end applications using React and Python.",
        "id": "kd_1",
        "keywords": [
          "React",
          "Python"
        ],
        "subtitle": "Day-to-day",
        "title": "Develop and maintain full stack applications"
      },
      {
        "category": "key-deliverable",
        "evidence": "Design and implement scalable and reliable backend services and APIs on the AWS cloud platform.",
        "id": "kd_2",
        "keywords": [
          "AWS",
          "API"
        ],
        "subtitle": "High impact",
        "title": "Design and implement AWS backend services"
      },
      {
        "category": "key-deliverable",
        "evidence": "Manage and deploy cloud resources using infrastructure-as-code tools like AWS CDK or Terraform.",
        "id": "kd_3",
        "keywords": [
          "AWS CDK",
          "Terraform"
        ],
        "subtitle": "Day-to-day",
        "title": "Manage cloud infrastructure as code"
      },
      {
        "category": "key-deliverable",
        "evidence": "Build and maintain robust unit and integration tests to ensure application stability.",
        "id": "kd_4",
        "keywords": [
          "Unit testing",
          "Integration testing"
        ],
        "subtitle": "Quality assurance",
        "title": "Build and maintain automated tests"
      }
    ],
    "missing_skills": [
      {
        "aliases": [],
        "in_must_have": True,
        "level": "required",
        "mentions": 1,
        "name": "JavaScript / TypeScript",
        "type": "skill"
      },
      {
        "aliases": [],
        "in_must_have": True,
        "level": "required",
        "mentions": 2,
        "name": "Python",
        "type": "skill"
      },
      {
        "aliases": [],
        "in_must_have": True,
        "level": "required",
        "mentions": 2,
        "name": "React.js",
        "type": "skill"
      },
      {
        "aliases": [],
        "in_must_have": True,
        "level": "required",
        "mentions": 4,
        "name": "AWS",
        "type": "skill"
      },
      {
        "aliases": [],
        "in_must_have": True,
        "level": "required",
        "mentions": 1,
        "name": "Infrastructure as Code",
        "type": "experience"
      },
      {
        "aliases": [],
        "in_must_have": True,
        "level": "preferred",
        "mentions": 1,
        "name": "Docker",
        "type": "skill"
      },
      {
        "aliases": [],
        "in_must_have": True,
        "level": "preferred",
        "mentions": 1,
        "name": "CI/CD",
        "type": "experience"
      }
    ],
    "must_haves": [
      {
        "aliases": [
          "Full-stack",
          "End-to-end"
        ],
        "category": "must-have",
        "evidence": "4 to 6 years of hands-on experience in building E2E applications",
        "id": "mh_1",
        "keywords": [
          "Full Stack",
          "E2E applications"
        ],
        "min_years": 4,
        "subtitle": "Core requirement",
        "title": "Full stack development experience"
      },
      {
        "aliases": [
          "ES6+",
          "JS"
        ],
        "category": "must-have",
        "evidence": "Strong proficiency in JavaScript (ES6+), TypeScript, and Python.",
        "id": "mh_2",
        "keywords": [
          "JavaScript",
          "TypeScript",
          "Python"
        ],
        "subtitle": "Core requirement",
        "title": "Proficiency in JavaScript, TypeScript, and Python"
      },
      {
        "aliases": [
          "React"
        ],
        "category": "must-have",
        "evidence": "Extensive experience with React.js for building responsive and dynamic user interfaces.",
        "id": "mh_3",
        "keywords": [
          "React.js",
          "Frontend"
        ],
        "subtitle": "Core requirement",
        "title": "React.js development"
      },
      {
        "aliases": [
          "Cloud"
        ],
        "category": "must-have",
        "evidence": "Hands-on experience with core AWS services, including Lambda, DynamoDB, S3, and API Gateway.",
        "id": "mh_4",
        "keywords": [
          "AWS",
          "Lambda",
          "DynamoDB"
        ],
        "subtitle": "Core requirement",
        "title": "AWS cloud services experience"
      },
      {
        "aliases": [
          "Python frameworks"
        ],
        "category": "must-have",
        "evidence": "Solid understanding of server-side development using Python frameworks such as Django or Flask.",
        "id": "mh_5",
        "keywords": [
          "Django",
          "Flask",
          "Backend"
        ],
        "subtitle": "Core requirement",
        "title": "Server-side development with Python frameworks"
      }
    ]
  }
}   
    company = 'AIRBUS'
    title = 'Full Stack Developer'
    structured_resume = {
  "output": {
    "personalDetails": {
      "fullName": "MANISH KUSHWAHA",
      "jobTitle": "Frontend Engineer",
      "email": "manishgtx1050@gmail.com",
      "phone": "+91 8826864321",
      "linkedin": "https://www.linkedin.com/in/manishgtx1050/"
    },
    "profileSummary": "Frontend Engineer | Data-Heavy Dashboards & Reporting Platforms| SQL · Python · Pandas",
    "education": [
      {
        "id": "edu-1",
        "degree": "BCA (Bachelor of Computer Applications)",
        "institution": "Amity University, Noida",
        "startDate": "Aug 2018",
        "endDate": "Dec 2021",
        "highlights": []
      }
    ],
    "workExperience": [
      {
        "id": "exp-1",
        "role": "Frontend Engineer",
        "company": "Unstop",
        "duration": "Sept 2023 – Aug 2025",
        "startDate": "Sept 2023",
        "endDate": "Aug 2025",
        "bullets": [
          {
            "id": 1,
            "text": "Co-built Unstop Bridge as one of two frontend engineers on the core team — an analytics dashboard platform connecting colleges, students, and recruiters — handling data visualization, filtering, search, and reporting flows across the hiring ecosystem.",
            "isInteractive": False
          },
          {
            "id": 2,
            "text": "Improved dashboard rendering performance by 20% by refactoring large Angular components (e.g., Search Filters) into modular child components, reducing change-detection overhead and supporting larger data loads without UX degradation.",
            "isInteractive": False
          },
          {
            "id": 3,
            "text": "Established a scalable component architecture and reusable patterns that evolved into the Unstop UI Library, reducing code duplication by 25% and enabling faster feature rollout across change cycles.",
            "isInteractive": False
          },
          {
            "id": 4,
            "text": "Enabled bulk student onboarding at scale by positioning TPO as the central data bridge — as more colleges joined, thousands of student records were ingested in a single flow, fueling rapid user growth and strengthening Unstop's hiring ecosystem.",
            "isInteractive": False
          },
          {
            "id": 5,
            "text": "Developed the AI Interview Report UI in Angular + PHP Blade, converting Figma designs into production-ready components that present candidate data and evaluation metrics at scale.",
            "isInteractive": False
          },
          {
            "id": 6,
            "text": "Redesigned and restructured reporting layer across AI Interviews, Psychometric, and Behavioral reports in PHP Blade, standardizing CSS and layouts to eliminate 30% redundant styles and deliver consistent data-presentation UI across web and PDF.",
            "isInteractive": False
          },
          {
            "id": 7,
            "text": "Collaborated with product and design teams to maintain design parity between Figma, Angular web views, and PDF report outputs.",
            "isInteractive": False
          },
          {
            "id": 8,
            "text": "Redesigned and integrated the AI-generated Mock Test application in React, replacing auto-generated layouts with Figma-driven UI; stabilized test flows and reduced candidate drop-offs during assessments.",
            "isInteractive": False
          },
          {
            "id": 9,
            "text": "Built responsive landing page for SBI Life's competition microsite from Figma designs, with client-specific tweaks for seamless Unstop integration. https://sbilifeideationx.com/",
            "isInteractive": False
          }
        ]
      },
      {
        "id": "exp-2",
        "role": "Frontend Developer",
        "company": "Thinnai",
        "duration": "Mar 2023 – Aug 2023",
        "startDate": "Mar 2023",
        "endDate": "Aug 2023",
        "bullets": [
          {
            "id": 1,
            "text": "Revamped UI of a React-based application to align with updated design guidelines; implemented new features improving application reliability and engagement.",
            "isInteractive": False
          }
        ]
      }
    ],
    "keySkills": {
      "languages": [
        "Python",
        "TypeScript",
        "JavaScript",
        "PHP",
        "HTML",
        "CSS",
        "SCSS"
      ],
      "libraries": [
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Express",
        "Angular",
        "Next.js",
        "React",
        "Redux Toolkit",
        "Tailwind",
        "Chart.js"
      ],
      "tools": [
        "MySQL",
        "PostgreSQL",
        "Jupyter",
        "Node.js",
        "Git",
        "GitHub",
        "Figma"
      ],
      "other": [
        "Statistics",
        "EDA",
        "REST APIs"
      ],
      "categories": [
        {
          "category": "Data & Analytics",
          "skills": [
            "SQL",
            "Python",
            "Pandas",
            "NumPy",
            "Statistics",
            "EDA",
            "Matplotlib",
            "Jupyter"
          ]
        },
        {
          "category": "Backend & APIs",
          "skills": [
            "Node.js",
            "Express",
            "REST APIs",
            "FastAPI",
            "PostgreSQL"
          ]
        },
        {
          "category": "Frontend",
          "skills": [
            "Angular",
            "Next.js",
            "React",
            "Redux Toolkit",
            "TypeScript",
            "JavaScript",
            "HTML",
            "CSS",
            "SCSS",
            "Tailwind",
            "Chart.js",
            "PHP"
          ]
        }
      ]
    },
    "projects": [],
    "internships": [],
    "certifications": [],
    "socialLinks": [],
    "languages": [],
    "hobbies": [],
    "extraCurricular": [],
    "leadership": [],
    "customSections": []
  }
}
    return compare_jd_resume(structured_jd, structured_resume,company,title)