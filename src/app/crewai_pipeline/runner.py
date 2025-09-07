from crewai import Crew, Process
from .agents import resume_score_builder_agent ,email_sender_agent
from .tasks import resume_score_builder_task ,email_sender_task
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import PyPDF2
import re
import os


about_company = "Nexus is software company that seeks for many position in the field of Technology and AI "
job_position = "Data Scientist"
level_experience = "Junior"
country_name = "Egypt"
job_description = '''
 Bachelor's or Master's degree in Data Science, Computer Science, Statistics, Mathematics, or a related field
 Proven experience as a Data Scientist or in a similar analytical role
 Strong programming skills in Python, R, or similar languages
 Proficiency in SQL and experience with relational and non-relational databases
 Experience with machine learning libraries and frameworks (e.g., Scikit-learn, TensorFlow, Keras)
 Knowledge of data visualization tools (e.g., Tableau, Power BI, matplotlib, seaborn) for communicating results
 Understanding of statistical concepts and methodologies, and experience applying them to real-world scenarios
 Excellent analytical and problem-solving skills
 Strong communication skills, both verbal and written, in English and Arabic
'''


def read_pdf_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def clean_resume_text(text: str) -> str:
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ ]{2,}', ' ', text)
    text = text.strip()
    return text

def run_nexus_crew(pdf_path: str , email: str):
    """Main entry: run CrewAI on a given resume PDF path."""
    raw_text = read_pdf_text(pdf_path)
    resume = clean_resume_text(raw_text)
    company_context = StringKnowledgeSource(
        content=about_company
    )
    nexus_crew = Crew(
    agents=[
        resume_score_builder_agent,
        email_sender_agent

    ],
    tasks=[
        resume_score_builder_task,
        email_sender_task

    ],
    process=Process.sequential,
    knowledge_sources=[company_context]
    )

    crew_results = nexus_crew.kickoff(
        inputs={
            "job_position": job_position,
            "level_experience": level_experience,
            "country_name": country_name,
            "job_description": job_description,
            "resume": resume,
            "email": email
        }
    )
    return crew_results