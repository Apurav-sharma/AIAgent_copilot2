"use client";

import { useEffect, useState } from "react";

const BACKEND_URL = "https://aiagent-copilot2.onrender.com";

export default function Page() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const [proposalId, setProposalId] = useState<string>("");
  const [proposal, setProposal] = useState<string | null>(null);
  const [options, setOptions] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  /* Load last used proposal_id */
  useEffect(() => {
    const stored = localStorage.getItem("proposal_id");
    if (stored) setProposalId(stored);
  }, []);

  async function sendMessage(text: string) {
    setMessages((m) => [...m, `You: ${text}`]);
    setLoading(true);

    const res = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: text,
        proposal_id: proposalId || null,
      }),
    });

    const data = await res.json();

    if (data?.proposal_id) {
      setProposalId(data.proposal_id);
      localStorage.setItem("proposal_id", data.proposal_id);
    }

    if (data?.response?.options) {
      setOptions(data.response.options);
    } else {
      setOptions(null);
    }

    if (data?.response?.draft) {
      setProposal(data.response.draft);
    }

    if (data?.response?.message) {
      setMessages((m) => [...m, `Agent: ${data.response.message}`]);
    }

    setInput("");
    setLoading(false);
  }

  function loadProposal() {
    setMessages([]);
    setProposal(null);
    setOptions(null);
    localStorage.setItem("proposal_id", proposalId);
  }

  function resetSession() {
    localStorage.removeItem("proposal_id");
    setProposalId("");
    setMessages([]);
    setProposal(null);
    setOptions(null);
  }

  return (
    <div className="h-screen bg-slate-950 text-slate-100 flex">
      {/* LEFT: CHAT */}
      <div className="w-1/3 border-r border-slate-800 flex flex-col">
        <div className="p-4 border-b border-slate-800 space-y-2">
          <div className="text-lg font-semibold">Copilot Chat</div>

          {/* Proposal ID Input */}
          <div className="flex gap-2">
            <input
              value={proposalId}
              onChange={(e) => setProposalId(e.target.value)}
              placeholder="Proposal ID"
              className="flex-1 bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs"
            />
            <button
              onClick={loadProposal}
              className="bg-slate-700 hover:bg-slate-600 px-2 py-1 rounded text-xs"
            >
              Load
            </button>
            <button
              onClick={resetSession}
              className="text-xs text-red-400 hover:text-red-300"
            >
              New
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2 text-sm">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={
                msg.startsWith("You")
                  ? "text-blue-400"
                  : "text-green-400"
              }
            >
              {msg}
            </div>
          ))}
          {loading && <div className="text-slate-400">Agent is thinking…</div>}
        </div>

        <div className="p-4 border-t border-slate-800 flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask Copilot…"
            className="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm"
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input || loading}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm"
          >
            Send
          </button>
        </div>
      </div>

      {/* CENTER: PROPOSAL */}
      <div className="w-1/3 p-6 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-2">Proposal Document</h2>

        {proposalId && (
          <div className="text-xs text-slate-400 mb-3">
            <b>Active Proposal ID:</b> {proposalId}
          </div>
        )}

        {proposal ? (
          <pre className="whitespace-pre-wrap text-sm bg-slate-900 border border-slate-800 rounded p-4">
            {proposal}
          </pre>
        ) : (
          <div className="text-slate-400 text-sm">
            No proposal loaded.
          </div>
        )}
      </div>

      {/* RIGHT: OPTIONS */}
      <div className="w-1/3 border-l border-slate-800 p-6">
        <h2 className="text-lg font-semibold mb-4">Agent Actions</h2>

        {options ? (
          <div className="space-y-2">
            <p className="text-sm text-slate-400 mb-2">
              Select a company:
            </p>
            {options.map((opt) => (
              <button
                key={opt.id}
                onClick={() => sendMessage(opt.name)}
                className="w-full bg-slate-900 border border-slate-700 hover:border-blue-500 rounded px-3 py-2 text-sm"
              >
                {opt.name}
              </button>
            ))}
          </div>
        ) : (
          <div className="text-slate-400 text-sm">
            No pending actions.
          </div>
        )}
      </div>
    </div>
  );
}
