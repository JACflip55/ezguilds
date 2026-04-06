import json
import os

import google.generativeai as genai

_model = None


def _get_model():
    global _model
    if _model is None:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        _model = genai.GenerativeModel("gemini-2.0-flash")
    return _model


def generate_next_question(
    goals: str | None,
    location: str | None,
    files_summary: list[str],
    previous_answers: list[dict],
) -> dict:
    model = _get_model()

    answers_text = ""
    if previous_answers:
        answers_text = "\n".join(
            f"Q: {a['question']}\nA: {a['answer']}" for a in previous_answers
        )

    prompt = f"""You are helping design a permaculture site plan. Based on the information provided, generate the single most important clarifying question that hasn't been asked yet.

User's uploaded files: {', '.join(files_summary) if files_summary else 'None'}
User's goals: {goals or 'Not provided'}
User's location: {location or 'Not provided'}

Previously asked questions and answers:
{answers_text or 'None yet'}

If goals or location have not been provided, prioritize asking for those first.
Consider what information would most improve the quality of a permaculture design.

Respond with JSON only:
{{"question": "Your question text", "why": "Brief explanation of why this matters for the design"}}"""

    response = model.generate_content(prompt)
    return json.loads(response.text)


def generate_chat_response(
    project_context: dict,
    chat_history: list[dict],
    new_message: str,
) -> dict:
    model = _get_model()

    history_text = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in chat_history
    )

    prompt = f"""You are an expert permaculture designer reviewing a site plan with the user.

Project context:
- Location: {project_context.get('location', 'Unknown')}
- Scale: {project_context.get('scale', 'Unknown')}
- Detail level: {project_context.get('detail_level', 'moderate')}
- Goals: {project_context.get('goals', 'Not specified')}

Chat history:
{history_text}

USER: {new_message}

Respond helpfully. If the user is requesting a design change, include "needs_regeneration": true in your response.

Respond with JSON only:
{{"response": "Your response text", "needs_regeneration": false}}"""

    response = model.generate_content(prompt)
    return json.loads(response.text)
