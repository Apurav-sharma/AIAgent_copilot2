from groq import Groq
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = Groq(api_key=API_KEY)

def extract_intent(query: str):
    prompt = f"""
Classify the user's intent and extract entity if present.

Possible intents:
- CREATE_PROPOSAL (start a new proposal)
- SELECT_COMPANY (user selects one of given companies)
- REVISE_PROPOSAL (modify an existing proposal)
- DONE (finish / acknowledge)
- UNKNOWN

Return ONLY valid JSON.

Schema:
{{
  "intent": "<INTENT>",
  "entity": "<company name if any, else empty>"
}}

User input:
"{query}"
"""
    try:
        res = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = res.choices[0].message.content.strip()
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return {
                "intent": data.get("intent", "UNKNOWN"),
                "entity": data.get("entity", "").strip(),
                "user_input": query.strip()
            }
    except:
        pass

    return {
        "intent": "UNKNOWN",
        "entity": "",
        "user_input": query.strip()
    }