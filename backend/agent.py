from data import find_company
from llm import generate_proposal, revise_proposal
from memory import reset_proposal

def run_agent(proposal, parsed):

    state = proposal["state"]
    intent = parsed["intent"]
    entity = parsed["entity"].lower() if parsed["entity"] else ""
    user_input = parsed["user_input"]

    # 🟢 CREATE PROPOSAL (only reset if fresh)
    if intent == "CREATE_PROPOSAL" and state == "INIT":
        if not entity:
            return {
                "message": "Starting a new proposal. Please specify the company name.",
                "expected": "COMPANY_NAME"
            }
        # entity exists → fall through to INIT logic

    # ✏️ REVISION
    if intent == "REVISE_PROPOSAL" and state == "DRAFT_READY":
        proposal["draft"] = revise_proposal(proposal["draft"], user_input)
        return {
            "message": "I’ve applied your requested changes.",
            "draft": proposal["draft"]
        }

    # ✅ DONE
    if intent == "DONE":
        return {
            "message": "Proposal is ready. You can revise it, approve it, or start a new proposal."
        }

    # 1️⃣ INIT — resolve company
    if state == "INIT":
        if not entity:
            return {
                "message": "Please provide the company name to continue.",
                "expected": "COMPANY_NAME"
            }

        matches = find_company(entity)

        if not matches:
            return {
                "message": f"I couldn’t find '{entity}'. Please provide a valid company name.",
                "expected": "COMPANY_NAME"
            }

        if len(matches) > 1:
            proposal["state"] = "NEED_COMPANY_CONFIRMATION"
            proposal["matches"] = matches
            return {
                "message": "Multiple companies found. Please select one.",
                "options": matches
            }

        proposal["company"] = matches[0]
        proposal["state"] = "CONTEXT_READY"

    # 2️⃣ CONFIRM COMPANY
    if state == "NEED_COMPANY_CONFIRMATION" and intent == "SELECT_COMPANY":
        for c in proposal["matches"]:
            if entity in c["name"].lower():
                proposal["company"] = c
                proposal["state"] = "CONTEXT_READY"
                break
        else:
            return {
                "message": "Please select one of the listed companies.",
                "options": proposal["matches"]
            }

    # 3️⃣ GENERATE PROPOSAL
    if proposal["state"] == "CONTEXT_READY":
        proposal["draft"] = generate_proposal(proposal["company"])
        proposal["state"] = "DRAFT_READY"
        return {
            "message": f"Proposal created for {proposal['company']['name']}.",
            "draft": proposal["draft"]
        }

    # 4️⃣ READY
    if proposal["state"] == "DRAFT_READY":
        return {
            "message": "Proposal is ready. You can revise it, approve it, or start a new proposal."
        }
