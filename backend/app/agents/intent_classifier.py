from app.services.gemini_service import model
from app.prompts.classify_prompt import classify_prompt

def classify_intent(email):

    response = model.generate_content(
        classify_prompt(email)
    )

    return response.text
