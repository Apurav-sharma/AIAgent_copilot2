from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from memory import create_proposal, get_proposal, returnall
from intent import extract_intent
from agent import run_agent
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    query: str
    proposal_id: Optional[str] = None


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
def chat(payload: ChatRequest):

    # Always ensure proposal exists
    proposal = None
    if payload.proposal_id:
        proposal = get_proposal(payload.proposal_id)

    if proposal is None:
        proposal_id = create_proposal()
        proposal = get_proposal(proposal_id)
    else:
        proposal_id = payload.proposal_id

    parsed = extract_intent(payload.query, proposal_id)
    response = run_agent(proposal, parsed)

    return {
        "proposal_id": proposal_id,
        "state": proposal["state"],
        "response": response
    }


@app.get("/getproposals")
def getpropo():
    return returnall()