from crewai import Agent, Task
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from .agents import basic_llm , email_sender_agent ,resume_score_builder_agent
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

output_dir = "outputs"  # make sure this folder exists

class ResumeScoreBuilder(BaseModel):
    score: float = Field(..., title="Read the given text to see whether he is suitable for job position or not")
    accepted: bool = Field(..., title="Read the given text to see whether he is suitable for job position or not")
    email: str = Field(...,title = "The email extracted from the candidate resume")

class GmailStructure(BaseModel):
    recipient: str = Field(..., title="The recipient of the email")
    subject: str = Field(..., title="The subject of the email")
    body: str = Field(..., title="The body of the email")    


resume_score_builder_task = Task(
    description="\n".join([
        "Nexus is looking to hire {job_position} as soon as possible (the candidate should match the requirements).",
        "The company target should be at {level_experience}.",
        "The candidate must reside in {country_name}.",
        "The company receives the {resume} and {email} to give a score out of 100 based on how much the candidate matches {job_description}.",
        "If the candidate has a score more than 90, they are accepted; otherwise, they are not.",
        "",
        "Return ONLY a JSON object in the format:",
        '{"score": 93, "accepted": true , "email": "candidate@example.com"}'
    ]),
    expected_output="JSON object with {score:int, accepted:bool, email:str}",
    output_json=ResumeScoreBuilder,
    output_file=os.path.join(output_dir, "step_1_resume_score_builder.json"),
    agent=resume_score_builder_agent,
)

email_sender_task = Task(
    description="\n".join([
        "You will receive JSON from the resume evaluator like:",
        '{"score": 93, "accepted": true}',
        "Use this JSON to craft a professional email which is sent to the candidate to {email}:",
        "- If accepted → send congratulations email.",
        "- If rejected → send polite rejection email.",
        "",
        "Return ONLY a JSON object with the following keys:",
        '{"recipient": "candidate@example.com", "subject": "Your application result", "body": "Dear Candidate, ..."}',
        "After returning the JSON, call the Send Email tool with: recipient|subject|body."
    ]),
    expected_output="JSON object with {recipient:str, subject:str, body:str}",
    output_json=GmailStructure,
    output_file=os.path.join(output_dir, "step_2_email_sender.json"),
    agent=email_sender_agent,
)
