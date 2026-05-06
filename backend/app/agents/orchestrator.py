from app.agents.intent_classifier import classify_intent
from app.agents.email_agent import generate_reply

from app.services.memory_service import (
    save_message,
    get_thread_memory
)

from app.services.email_service import send_email


def process_email(
    thread_id,
    sender_email,
    subject,
    incoming_message,
    budget
):

    # STEP 1 — classify intent
    intent = classify_intent(incoming_message)

    # STEP 2 — save incoming email
    save_message(
        thread_id=thread_id,
        sender="prospect",
        subject=subject,
        body=incoming_message,
        intent=intent
    )

    # STEP 3 — fetch previous memory
    memory = get_thread_memory(thread_id)

    memory_text = ""

    for msg in memory:

        memory_text += f"""
        {msg.sender}:
        {msg.body}
        """

    ai_reply = generate_reply(
    memory_text,
    incoming_message,
    budget,
    intent
)

    # STEP 5 — send email
    send_email(
        sender_email,
        f"Re: {subject}",
        ai_reply
    )

    # STEP 6 — save AI reply
    save_message(
        thread_id=thread_id,
        sender="agent",
        subject=f"Re: {subject}",
        body=ai_reply
    )

    return {
        "intent": intent,
        "reply": ai_reply
    }