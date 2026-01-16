COMPANIES = [
    {
        "id": "1",
        "name": "yellow.ai",
        "industry": "AI SaaS",
        "product": "Conversational AI Platform",
        "deal_value": "$150,000"
    },
    {
        "id": "2",
        "name": "yellow.ai Singapore",
        "industry": "AI SaaS (APAC)",
        "product": "Enterprise Chatbot Suite",
        "deal_value": "$180,000"
    },
    {
        "id": "3",
        "name": "data robot",
        "industry": "AI SaaS (APAC)",
        "product": "Enterprise Chatbot Suite",
        "deal_value": "$240,000"
    }
]

def find_company(name):
    return [c for c in COMPANIES if name and name.lower() in c["name"].lower()]
