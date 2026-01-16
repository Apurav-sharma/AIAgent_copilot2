import uuid

PROPOSALS = {}

def create_proposal():
    pid = str(uuid.uuid4())
    PROPOSALS[pid] = {
        "state": "INIT",
        "company": None,
        "matches": None,
        "draft": None
    }
    return pid

def get_proposal(pid):
    return PROPOSALS.get(pid)
