from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import tool
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
import agentops
from pydantic import BaseModel, Field
from typing import List
import os
import json
from dotenv import load_dotenv
from .tools import GmailSendTool
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

email_tool = GmailSendTool()
agentops.init(
    api_key=os.getenv('AGENTOPS_API_KEY'),
    skip_auto_end_session=True,
    default_tags=['crewai']
)

basic_llm = LLM(
    model="openai/gpt-oss-20b:free",
    base_url="https://openrouter.ai/api/v1",

    api_key=os.environ["OPENROUTER_API_KEY"],
    temperature= 0
    )

resume_score_builder_agent =Agent(
    role="Job Recuriment Agent",
    goal="\n".join([
                "To get resumes and to decide whether the candidate is suitable for the position and to give score for how much he is a good fit",

            ]),
    backstory="The agent is designed to help in looking for good candidate for the {job_position} ",
    llm=basic_llm,
    verbose=True,
)

email_sender_agent = Agent(
    role="Email Writer",
    goal="Send professional acceptance or rejection emails",
    backstory="This agent takes candidate results and sends proper Gmail messages",
    llm=basic_llm,
    verbose=True,
    tools=[email_tool]
)