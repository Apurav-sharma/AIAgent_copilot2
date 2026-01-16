from data import find_company
from llm import generate_proposal

def run_agent(proposal, parsed_input):

    state = proposal["state"]
    user_text = (parsed_input.get("entity") or "").lower()

    # INIT: resolve company
    if state == "INIT":
        matches = find_company(user_text)

        if not matches:
            return {
                "message": f"I couldn't find a company named '{user_text}'. Please provide a valid company name."
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

    # Company selection
    if proposal["state"] == "NEED_COMPANY_CONFIRMATION":
        for c in proposal["matches"]:
            if c["name"] and user_text in c["name"].lower():
                proposal["company"] = c
                proposal["state"] = "CONTEXT_READY"
                break
        else:
            return {
                "message": "Please select one of the listed companies.",
                "options": proposal["matches"]
            }

    # Generate proposal
    if proposal["state"] == "CONTEXT_READY":
        proposal["draft"] = generate_proposal(proposal["company"])
        proposal["state"] = "DRAFT_READY"
        return {
            "message": f"Proposal created for {proposal['company']['name']}.",
            "draft": proposal["draft"]
        }

    # Draft ready
    if proposal["state"] == "DRAFT_READY":
        return {
            "message": "Proposal is ready. You can ask for revisions or approval."
        }
