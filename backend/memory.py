import uuid

PROPOSALS = {}

chat_history = {}

def create_proposal():
    pid = str(uuid.uuid4())
    PROPOSALS[pid] = {
        "state": "INIT",
        "company": None,
        "matches": None,
        "draft": None
    }
    chat_history[pid] = []
    return pid

def get_proposal(pid):
    return PROPOSALS.get(pid)

def get_chat_history(pid):
    return chat_history.get(pid, [])

def reset_proposal(proposal):
    proposal["state"] = "INIT"
    proposal["company"] = None
    proposal["matches"] = []
    proposal["draft"] = ""

def returnall():
    return PROPOSALS