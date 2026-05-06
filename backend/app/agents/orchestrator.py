from app.agents.intent_classifier import classify_intent
from app.agents.email_agent import generate_reply
from app.agents.reschedule import handle_reschedule_edge_case

from app.services.memory_service import (
    save_message,
    get_thread_memory
)

from app.services.email_service import send_email


def format_memory_for_context(messages):
    """
    Format message history in a way that helps the AI understand context.
    Include sender, intent, and body for better conversation continuity.
    """
    if not messages:
        return "(No prior conversation history)"

    formatted = []
    for msg in messages:
        intent_label = f" [{msg.intent}]" if msg.intent else ""
        formatted.append(f"{msg.sender.upper()}{intent_label}:\n{msg.body}")

    return "\n\n".join(formatted)


def process_email(
    thread_id,
    sender_email,
    subject,
    incoming_message,
    budget
):
    """
    Main email processing pipeline with conversation quality focus:
    1. Classify intent from incoming message
    2. Save incoming message to thread history
    3. Fetch and format conversation memory
    4. Check for reschedule edge cases (repeated cancellations, etc.)
    5. Generate contextual AI reply
    6. Send the reply
    7. Save AI response to history
    """

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

    # STEP 3 — fetch and format previous memory
    memory_messages = get_thread_memory(thread_id)
    memory_text = format_memory_for_context(memory_messages)

    # STEP 4 — check for reschedule edge cases
    edge_case_note = handle_reschedule_edge_case(
        thread_id=thread_id,
        latest_intent=intent,
        messages=memory_messages
    )

    if edge_case_note:
        memory_text += f"\n\n[INTERNAL NOTE: {edge_case_note}]"

    # STEP 5 — generate contextual reply
    ai_reply = generate_reply(
        memory=memory_text,
        latest_message=incoming_message,
        budget=budget,
        intent=intent
    )

    # STEP 6 — send email
    send_email(
        sender_email,
        f"Re: {subject}",
        ai_reply
    )

    # STEP 7 — save AI reply to thread history
    save_message(
        thread_id=thread_id,
        sender="agent",
        subject=f"Re: {subject}",
        body=ai_reply,
        intent="response"
    )

    return {
        "intent": intent,
        "reply": ai_reply,
        "edge_case_detected": bool(edge_case_note)
    }
