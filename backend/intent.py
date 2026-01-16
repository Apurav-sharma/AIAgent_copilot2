from groq import Groq
import json
import re
from concurrent.futures import process


API_KEY = process.env.GROQ_API_KEY

client = Groq(api_key=API_KEY)

def extract_intent(query: str):
    prompt = f"""
You are a JSON API.

Extract intent and entity from the user query.

Return ONLY valid JSON.
No text. No explanation.

Schema:
{{
  "intent": "CREATE_PROPOSAL",
  "entity": "<company name>"
}}

User query:
"{query}"
"""

    res = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = res.choices[0].message.content.strip()

    # 🛡️ SAFETY: extract JSON even if model adds text
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if not match:
        # fallback (never crash agent)
        return {
            "intent": "UNKNOWN",
            "entity": query
        }

    return json.loads(match.group())
