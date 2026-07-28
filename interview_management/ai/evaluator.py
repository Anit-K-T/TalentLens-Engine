import json
import google.generativeai as genai
from django.conf import settings

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-flash-latest")



def evaluate_interview(transcript):
    """
    Evaluate interview transcript using Gemini.
    """

    prompt = f"""
You are an expert HR interviewer.

Analyze the following interview transcript.

Return ONLY valid JSON in exactly this format:

{{
    "communication_score": 0,
    "technical_score": 0,
    "confidence_score": 0,
    "overall_score": 0,
    "hiring_recommendation": "",
    "strengths": [
        "",
        "",
        ""
    ],
    "weaknesses": [
        "",
        "",
        ""
    ],
    "summary": "",
    "ai_feedback": ""
}}

Rules:
- Scores must be between 0 and 100.
- Recommendation must be one of:
  Strong Hire
  Hire
  Hold
  Reject
- Feedback should be concise (3–5 sentences).
- Return JSON only. Do not include markdown or explanations.

Transcript:
{transcript}
"""

    try:
        response = model.generate_content(prompt)
    except Exception as e:
        print("Gemini Error:", e)
        raise

    print("=" * 50)
    print("RAW GEMINI RESPONSE:")
    print(response.text)
    print("=" * 50)

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    print("PARSED TEXT:")
    print(text)

    result = json.loads(text)
    print("=" * 50)
    print(result)
    print("=" * 50)

    print("RESULT DICTIONARY:")
    print(result)

    return result