"use client";
import { useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const API_URL = process.env.NEXT_PUBLIC_API_URL;
  const handleSend = async () => {
    setResponse("Loading...");

    const result = await fetch(API_URL + "/chat", {
      method: "POST",
      body: JSON.stringify({ query: message }),
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await result.json();
    setResponse(data);
  };

  return (
    <main>
      <h1>DostoevskyAI</h1>

      <div>
        <input
          type="text"
          placeholder="Enter your message..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        />
        <button onClick={handleSend}>Send</button>
      </div>

      <div>{response}</div>
    </main>
  );
}
