from groq import Groq
import json
import re
from dotenv import load_dotenv
from memory import chat_history
import os

load_dotenv()


API_KEY = os.getenv("API_KEY")

client = Groq(api_key=API_KEY)

def extract_intent(query: str, proposal_id: str):
    prompt = f"""
Classify the user's intent and extract entity if present.

Possible intents:
- CREATE_PROPOSAL (start a new proposal)
- SELECT_COMPANY
- REVISE_PROPOSAL (modify an existing proposal)
- DONE (finish / acknowledge)

Return ONLY valid JSON.

Schema:
{{
  "intent": "<INTENT>",
  "entity": "<company name if any, else empty>"
}}

User input:
"{query}"
previous hostory:
"{chat_history[proposal_id]}

"""
    try:
        res = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[{"role": "user", "content": prompt}]
        )

        raw = res.choices[0].message.content.strip()
        chat_history[proposal_id].append({"user" : query, "output": raw})

        if(len(chat_history[proposal_id]) > 20):
            chat_history[proposal_id].pop(0)

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