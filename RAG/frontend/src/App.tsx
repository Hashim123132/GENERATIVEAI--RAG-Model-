import React, { useState } from "react";
import "./App.css";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";

type Message = { role: "user" | "assistant"; text: string };

function App(): JSX.Element {
  const [messages, setMessages] = useState<Message[]>([]);

  async function handleSend(question: string) {
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: data.answer },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", text: "Error contacting server." },
      ]);
    }
  }

  return (
    <div className="app root">
      <div className="container">
        <h1 className="title">RAG Chat</h1>
        <ChatWindow messages={messages} />
        <ChatInput onSend={handleSend} />
      </div>
    </div>
  );
}

export default App;
