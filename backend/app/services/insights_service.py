
import requests
from app.config import settings

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash-lite:generateContent"

def get_borrower_insights(applicant_data: dict) -> dict:
    """
    Calls Gemini API with applicant data and returns structured insights for dashboard.
    """
    GEMINI_API_KEY = settings.gemini_api_key
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in environment.")
    # Compose prompt for Gemini
    prompt = f"""
    Given the following applicant data, generate a detailed Borrower Intelligence Report organized into these 6 categories: Financial Health, Work Performance, Behavioral Signals, Identity & Fraud, Network Insights, Risk Assessment. For each, provide the same metrics and format as the sample dashboard. Also provide a final dashboard output with recommendation, reasoning, suggested terms, confidence, and top 5 factors influencing decision.

    Respond ONLY with a valid JSON object, no markdown, no explanation, no code block, no extra text. The response must be directly parsable as JSON.

    Applicant Data: {applicant_data}
    """
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 2048}
    }
    response = requests.post(
        f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
        headers=headers,
        json=payload
    )
    response.raise_for_status()
    result = response.json()
    # Extract the model's reply (handle plain text, markdown, or fallback)
    import re, json as pyjson
    try:
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        # Try to extract JSON from a markdown code block
        match = re.search(r"```json\\s*(.*?)```", text, re.DOTALL)
        if match:
            return pyjson.loads(match.group(1))
        # Try to extract JSON from any code block
        match = re.search(r"```[a-zA-Z]*\\s*(.*?)```", text, re.DOTALL)
        if match:
            return pyjson.loads(match.group(1))
        # Try to parse as JSON directly
        return pyjson.loads(text)
    except Exception:
        # Fallback: try to parse JSON from raw_text if present
        raw_text = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if raw_text:
            # Remove code block markers if present
            raw_text_clean = re.sub(r"^```json|^```|```$", "", raw_text.strip(), flags=re.MULTILINE).strip()
            try:
                return pyjson.loads(raw_text_clean)
            except Exception:
                pass
        # Fallback: return the raw text for debugging
        return {"error": "Failed to parse Gemini response", "raw": result, "raw_text": raw_text}