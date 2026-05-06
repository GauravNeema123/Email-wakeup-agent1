from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.thread_service import (
    create_prospect,
    create_thread,
    get_prospect,
    get_thread,
    list_prospects,
    list_threads,
    update_thread,
)
from app.services.memory_service import get_thread_memory

router = APIRouter(prefix="/threads", tags=["Threads"])


class ProspectCreateRequest(BaseModel):
    name: str
    email: str


class ThreadCreateRequest(BaseModel):
    prospect_id: int
    budget_ceiling: int
    current_state: Optional[str] = "NEW"
    scheduled_time: Optional[str] = None


class ThreadUpdateRequest(BaseModel):
    current_state: Optional[str] = None
    budget_ceiling: Optional[int] = None
    scheduled_time: Optional[str] = None


def prospect_to_dict(prospect):
    return {
        "id": prospect.id,
        "name": prospect.name,
        "email": prospect.email,
        "status": prospect.status,
    }


def thread_to_dict(thread):
    return {
        "id": thread.id,
        "prospect_id": thread.prospect_id,
        "current_state": thread.current_state,
        "budget_ceiling": thread.budget_ceiling,
        "scheduled_time": thread.scheduled_time,
    }


@router.get("/prospects")
def list_all_prospects():
    prospects = list_prospects()
    return [prospect_to_dict(prospect) for prospect in prospects]


@router.get("/prospects/{prospect_id}")
def get_prospect_route(prospect_id: int):
    prospect = get_prospect(prospect_id)
    if prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")
    return prospect_to_dict(prospect)


@router.post("/prospects")
def create_prospect_route(data: ProspectCreateRequest):
    prospect = create_prospect(data.name, data.email)
    return prospect_to_dict(prospect)


@router.get("/")
def list_all_threads():
    threads = list_threads()
    return [thread_to_dict(thread) for thread in threads]


@router.post("/")
def create_thread_route(data: ThreadCreateRequest):
    prospect = get_prospect(data.prospect_id)
    if prospect is None:
        raise HTTPException(status_code=404, detail="Prospect not found")
    thread = create_thread(
        prospect_id=data.prospect_id,
        budget_ceiling=data.budget_ceiling,
        current_state=data.current_state,
        scheduled_time=data.scheduled_time,
    )
    return thread_to_dict(thread)


@router.get("/{thread_id}")
def get_thread_route(thread_id: int):
    thread = get_thread(thread_id)
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    messages = get_thread_memory(thread_id)
    return {
        **thread_to_dict(thread),
        "messages": [
            {
                "id": message.id,
                "sender": message.sender,
                "subject": message.subject,
                "body": message.body,
                "intent": message.intent,
            }
            for message in messages
        ],
    }


@router.patch("/{thread_id}")
def update_thread_route(thread_id: int, data: ThreadUpdateRequest):
    thread = update_thread(
        thread_id,
        current_state=data.current_state,
        budget_ceiling=data.budget_ceiling,
        scheduled_time=data.scheduled_time,
    )
    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread_to_dict(thread)
