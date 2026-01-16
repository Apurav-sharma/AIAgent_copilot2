const BACKEND_URL = "http://localhost:8000";

export async function sendMessage(query: string, proposalId?: string) {
  const res = await fetch(`${BACKEND_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query,
      proposal_id: proposalId,
    }),
  });

  return res.json();
}
