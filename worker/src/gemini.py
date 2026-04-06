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


def generate_design(prompt: str) -> dict:
    model = _get_model()
    response = model.generate_content(prompt)
    text = response.text
    # Strip markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        text = text.rsplit("```", 1)[0]
    return json.loads(text)
