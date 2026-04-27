import React, { useState } from "react";

export default function ChatInput({ onSend }: { onSend: (q: string) => void }) {
  const [value, setValue] = useState("");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (!value.trim()) return;
    onSend(value.trim());
    setValue("");
  }

  return (
    <form className="chat-input" onSubmit={submit}>
      <input
        aria-label="Ask a question"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Ask about the document..."
      />
      <button type="submit">Send</button>
    </form>
  );
}
