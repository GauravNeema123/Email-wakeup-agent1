from app.services.gemini_service import model

from app.prompts.response_prompt import (
    response_prompt
)

from app.agents.scheduler import (
    get_available_slots
)


def generate_reply(
    memory,
    latest_message,
    budget,
    intent
):

    slots = get_available_slots()

    slots_text = "\n".join(
        [f"- {slot}" for slot in slots]
    )

    prompt = response_prompt(
        memory=memory,
        latest_message=latest_message,
        budget=budget,
        intent=intent,
        slots=slots_text
    )

    response = model.generate_content(
        prompt
    )

    return response.text