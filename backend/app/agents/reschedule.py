"""
Reschedule edge case handler — detects and flags problematic patterns:
- Multiple cancellations in a row
- Conflicting availability statements
- Ambiguous objections (hesitation vs. hard decline)
"""


def handle_reschedule_edge_case(thread_id, latest_intent, messages):
    """
    Analyze conversation for reschedule edge cases.
    Returns a string note if an edge case is detected, else None.
    """

    if not messages:
        return None

    # Count reschedule and decline intents in recent history
    recent_count = min(10, len(messages))
    reschedule_count = sum(
        1 for m in messages[-recent_count:] if m.intent == "reschedule"
    )
    decline_count = sum(
        1 for m in messages[-recent_count:] if m.intent == "decline"
    )

    # EDGE CASE 1: Repeated rescheduling (3+ times)
    if reschedule_count >= 3:
        return (
            "Prospect has rescheduled multiple times. "
            "Be empathetic but firm: acknowledge the pattern gently, "
            "suggest ONE final slot or offer async alternatives."
        )

    # EDGE CASE 2: Decline followed by continued engagement
    if decline_count > 0 and latest_intent not in ["decline"]:
        last_decline_idx = len(messages) - 1
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].intent == "decline":
                last_decline_idx = i
                break
        messages_after_decline = len(messages) - last_decline_idx - 1
        if messages_after_decline > 0:
            return (
                "Prospect previously declined but re-engaged. "
                "This is a second chance — be warm and specific, "
                "don't restate the full pitch."
            )

    # EDGE CASE 3: Ambiguous objection (asking_question after negotiating)
    if latest_intent == "asking_question":
        recent_intents = [m.intent for m in messages[-5:] if m.intent]
        if "negotiating" in recent_intents:
            return (
                "Prospect is asking clarifying questions after negotiating. "
                "They may be warming up — answer concisely and suggest a call."
            )

    return None
