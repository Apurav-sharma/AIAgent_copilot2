from groq import Groq
from dotenv import load_dotenv
import os
from memory import chat_history

load_dotenv()

API_KEY = os.getenv("API_KEY")

client = Groq(api_key=API_KEY)

def generate_proposal(company):
    prompt = f"""
You are an enterprise sales proposal agent.

Company details:
Name: {company['name']}
Industry: {company['industry']}
Product: {company['product']}
Deal Value: {company['deal_value']}

Write a professional sales proposal with:
1. Executive Summary
2. Problem Statement
3. Proposed Solution
4. Pricing
5. Timeline
"""

    res = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}]
    )

    chat_history.append({"user" : prompt, "output": res.choices[0].message.content})
    if(len(chat_history) > 20):
        chat_history.pop(0)

    return res.choices[0].message.content


def revise_proposal(draft: str, instruction: str):
    prompt = f"""
You are revising an existing enterprise sales proposal.

CURRENT PROPOSAL:
{draft}

USER REQUEST:
{instruction}

Apply the requested change carefully.
Return the FULL revised proposal.
"""
    res = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content