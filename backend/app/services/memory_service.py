from app.database.connection import SessionLocal
from app.database.models import Message


def save_message(
    thread_id,
    sender,
    subject,
    body,
    intent=None
):

    db = SessionLocal()

    message = Message(
        thread_id=thread_id,
        sender=sender,
        subject=subject,
        body=body,
        intent=intent
    )

    db.add(message)

    db.commit()

    db.refresh(message)

    db.close()

    return message


def get_thread_memory(thread_id):

    db = SessionLocal()

    messages = db.query(Message).filter(
        Message.thread_id == thread_id
    ).all()

    db.close()

    return messages