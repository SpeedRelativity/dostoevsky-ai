"use client";
import { useState } from "react";
import { useEffect } from "react";

export default function Home() {
  const [message, setMessage] = useState("What's on your mind?");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>(
    [],
  );

  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const handleSend = async () => {
    if (!message.trim()) return; // Don't send empty messages

    const userText = message;
    const history = messages;

    setMessages((prev) => [...prev, { role: "user", content: userText }]);
    setMessage("");
    setLoading(true);

    try {
      const result = await fetch(API_URL + "/chat", {
        method: "POST",
        body: JSON.stringify({
          query: message,
          history: history,
          session_id: sessionId,
        }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await result.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data }]);
    } catch (error) {
      console.error("Error occured: ", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let id = localStorage.getItem("dostoevsky_session_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("dostoevsky_session_id", id);
    }
    setSessionId(id);
  }, []);

  return (
    <main className="min-h-screen bg-[#f4ecd8] text-[#3a2e22] font-serif flex flex-col items-center px-6 py-16">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <header className="text-center mb-10 border-b border-[#c9b896] pb-8">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-[#2b211a]">
            Fyodor Dostoevsky AI
          </h1>
          <p className="mt-3 text-base sm:text-lg italic text-[#6b5844]">
            If its taking a while, please wait (I have free backend server, its
            slow...)
          </p>
        </header>

        {/* Input row */}
        <div className="flex flex-col sm:flex-row gap-3 mb-8">
          <input
            type="text"
            placeholder="Ask your question..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            disabled={loading}
            className="flex-1 px-4 py-3 rounded-md bg-[#fbf6ea] border border-[#c9b896] text-[#3a2e22] placeholder:text-[#a8957c] focus:outline-none focus:border-[#8a6f4d] focus:ring-1 focus:ring-[#8a6f4d] disabled:opacity-60 transition"
          />
          <button
            onClick={handleSend}
            disabled={loading}
            className="px-6 py-3 rounded-md bg-[#6b4f2e] text-[#f4ecd8] font-medium tracking-wide hover:bg-[#553d22] active:bg-[#43301a] disabled:opacity-50 disabled:cursor-not-allowed transition whitespace-nowrap"
          >
            {loading ? "Thinking..." : "Speak"}
          </button>
        </div>

        {/* Conversation thread */}
        <div className="flex flex-col gap-4 bg-[#ece0c4] border border-[#d6c39c] rounded-lg p-5 min-h-[120px]">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={
                msg.role === "user"
                  ? "self-end max-w-[85%] rounded-md bg-[#6b4f2e] text-[#f4ecd8] px-4 py-3"
                  : "self-start max-w-[85%] rounded-md bg-[#fbf6ea] border border-[#c9b896] text-[#3a2e22] px-5 py-4 shadow-sm"
              }
            >
              <p className="leading-relaxed whitespace-pre-wrap">
                {msg.content}
              </p>
            </div>
          ))}

          {loading && (
            <div className="self-start max-w-[85%] rounded-md bg-[#fbf6ea] border border-[#c9b896] px-5 py-4 shadow-sm">
              <p className="italic text-[#a8957c] animate-pulse">
                The master gathers his thoughts...
              </p>
            </div>
          )}
        </div>

        {/* Clear conversation */}
        {messages.length > 0 && (
          <button
            onClick={() => setMessages([])}
            className="mt-6 text-sm text-[#8a6f4d] hover:text-[#553d22] underline transition"
          >
            Clear conversation
          </button>
        )}

        {/* Transparency note */}
        <p className="mt-10 text-xs text-center text-[#a8957c] italic">
          Questions are logged anonymously to improve this guide.
        </p>
      </div>
    </main>
  );
}
