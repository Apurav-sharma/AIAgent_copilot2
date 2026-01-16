"use client";

import { useState } from "react";

export default function ChatBox({ messages, onSend }: any) {
  const [input, setInput] = useState("");

  return (
    <div style={{ width: "30%", padding: 16, borderRight: "1px solid #333" }}>
      <h3>Copilot Chat</h3>

      <div style={{ height: "80%", overflowY: "auto" }}>
        {messages.map((m: string, i: number) => (
          <p key={i}>{m}</p>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask Copilot..."
        style={{ width: "100%", marginTop: 8 }}
      />

      <button
        onClick={() => {
          onSend(input);
          setInput("");
        }}
        style={{ width: "100%", marginTop: 8 }}
      >
        Send
      </button>
    </div>
  );
}
