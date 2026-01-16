"use client";

import { useState } from "react";

const BACKEND_URL = "http://localhost:8000";

export default function Page() {
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");
  const [proposalId, setProposalId] = useState<string | null>(null);
  const [proposal, setProposal] = useState<string | null>(null);
  const [options, setOptions] = useState<any[] | null>(null);
  const [loading, setLoading] = useState(false);

  async function sendMessage(text: string) {
    setMessages((m) => [...m, `You: ${text}`]);
    setLoading(true);

    const res = await fetch(`${BACKEND_URL}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: text,
        proposal_id: proposalId,
      }),
    });

    const data = await res.json();

    setProposalId(data.proposal_id ?? proposalId);

    // OPTIONS (company selection)
    if (data?.response?.options) {
      setOptions(data.response.options);
    } else {
      setOptions(null);
    }

    // PROPOSAL DRAFT
    if (data?.response?.draft) {
      setProposal(data.response.draft);
    }

    // SAFE AGENT MESSAGE

    if (data?.response?.message) {
      setMessages((m) => [...m, `Agent: ${data.response.message}`]);
    }

    setInput("");
    setLoading(false);
  }


  return (
    <div className="h-screen bg-slate-950 text-slate-100 flex">
      {/* LEFT: CHAT */}
      <div className="w-1/3 border-r border-slate-800 flex flex-col">
        <div className="p-4 border-b border-slate-800 text-lg font-semibold">
          Copilot Chat
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2 text-sm">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`${msg.startsWith("You")
                ? "text-blue-400"
                : "text-green-400"
                }`}
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
            className="flex-1 bg-slate-900 border border-slate-700 rounded px-3 py-2 text-sm outline-none"
          />
          <button
            onClick={() => sendMessage(input)}
            disabled={!input || loading}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-sm disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>

      {/* CENTER: PROPOSAL */}
      <div className="w-1/3 p-6 overflow-y-auto">
        <h2 className="text-lg font-semibold mb-4">Proposal Document</h2>

        {proposal ? (
          <pre className="whitespace-pre-wrap text-sm bg-slate-900 border border-slate-800 rounded p-4">
            {proposal}
          </pre>
        ) : (
          <div className="text-slate-400 text-sm">
            Proposal will appear here once generated.
          </div>
        )}
      </div>

      {/* RIGHT: OPTIONS */}
      <div className="w-1/3 border-l border-slate-800 p-6">
        <h2 className="text-lg font-semibold mb-4">Agent Actions</h2>

        {options ? (
          <div className="space-y-2">
            <p className="text-sm text-slate-400 mb-2">
              Multiple companies found. Select one:
            </p>

            {options.map((opt) => (
              <button
                key={opt.id}
                onClick={() => sendMessage(opt.name)}
                className="w-full text-left bg-slate-900 border border-slate-700 hover:border-blue-500 rounded px-3 py-2 text-sm"
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
