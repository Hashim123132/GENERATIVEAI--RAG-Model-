import React, { useEffect, useRef } from "react";

type Message = { role: "user" | "assistant"; text: string };

export default function ChatWindow({ messages }: { messages: Message[] }) {
  const endRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="empty">Ask a question to start the conversation.</div>
      )}
      {messages.map((m, i) => (
        <div key={i} className={`msg ${m.role}`}>
          <div className="bubble">{m.text}</div>
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
}
