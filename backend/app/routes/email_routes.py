# email_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from app.agents.orchestrator import process_email
from app.services.email_service import send_email

router = APIRouter(prefix="/email", tags=["Email"])


# Add this model
class EmailProcessRequest(BaseModel):
    thread_id: int
    sender_email: str
    subject: str
    message: str
    budget: float


class OutreachRequest(BaseModel):
    name: str
    email: str


@router.get("/")
def home():
    return {"message": "Email routes working"}


@router.post("/process")
def process(data: EmailProcessRequest):      # ← typed, not dict
    result = process_email(
        thread_id=data.thread_id,
        sender_email=data.sender_email,
        subject=data.subject,
        incoming_message=data.message,
        budget=data.budget
    )
    return result


@router.post("/outreach")
def outreach(data: OutreachRequest):         # ← same here
    subject = "AI Fullstack Engineer Opportunity"
    body = f"""
    Hi {data.name},
    ...
    """
    send_email(data.email, subject, body)
    return {"message": "Outreach email sent"}