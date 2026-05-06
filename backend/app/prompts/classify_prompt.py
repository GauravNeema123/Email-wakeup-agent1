def classify_prompt(email):

    return f"""
You are an AI email intent classifier.

Classify the email into ONE of these:

- interested
- negotiating
- reschedule
- decline
- asking_question

Rules:
- Output ONLY one word
- No explanation
- No punctuation

Email:
{email}
"""