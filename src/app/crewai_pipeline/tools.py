import os
import smtplib
from email.mime.text import MIMEText
from crewai.tools import BaseTool
from crewai.tools import BaseTool
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../../.env"))

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")


class GmailSendTool(BaseTool):
    name: str = "Send Email"
    description: str = "Send an email via Gmail. Input format: recipient|subject|body"

    def _run(self, query: str) -> str:
        try:
            to, subject, body = query.split("|",2)

            msg = MIMEText(body)
            msg["From"] = EMAIL
            msg["To"] = to
            msg["Subject"] = subject

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(EMAIL, APP_PASSWORD)
                server.send_message(msg)

            return f"✅ Email sent to {to} with subject '{subject}'"
        except Exception as e:
            return f"❌ Failed to send email: {e}"