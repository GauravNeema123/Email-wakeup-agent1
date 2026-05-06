from app.services.gemini_service import model
from app.prompts.response_prompt import response_prompt


def generate_reply(memory, latest_message, budget, intent):

    prompt = response_prompt(
        memory=memory,
        latest_message=latest_message,
        budget=budget,
        intent=intent
    )

    response = model.generate_content(prompt)

    return response.text.strip()