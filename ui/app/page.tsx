"use client";
import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const handleSend = async () => {
    if (!message.trim()) return; // Don't send empty messages

    setLoading(true);
    setResponse("");

    try {
      const result = await fetch(API_URL + "/chat", {
        method: "POST",
        body: JSON.stringify({ query: message }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      const data = await result.json();
      setResponse(data);
    } catch (error) {
      console.error("Error occured: ", error);
      setResponse("Something's off. Try again or bugged. Sorry.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-[#f4ecd8] text-[#3a2e22] font-serif flex flex-col items-center px-6 py-16">
      <div className="w-full max-w-2xl">
        {/* Header */}
        <header className="text-center mb-10 border-b border-[#c9b896] pb-8">
          <h1 className="text-4xl sm:text-5xl font-bold tracking-tight text-[#2b211a]">
            Fyodor Dostoevsky
          </h1>
          <p className="mt-3 text-base sm:text-lg italic text-[#6b5844]">
            A guide for the troubled soul
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

        {/* Response */}
        {(response || loading) && (
          <div className="rounded-md bg-[#fbf6ea] border border-[#c9b896] shadow-sm px-6 py-6">
            {loading ? (
              <p className="italic text-[#a8957c] animate-pulse">
                The master gathers his thoughts...
              </p>
            ) : (
              <p className="text-lg leading-relaxed whitespace-pre-wrap text-[#3a2e22]">
                {response}
              </p>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
