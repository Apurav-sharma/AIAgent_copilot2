from concurrent.futures import process
from groq import Groq

API_KEY = process.env.GROQ_API_KEY

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

    return res.choices[0].message.content
