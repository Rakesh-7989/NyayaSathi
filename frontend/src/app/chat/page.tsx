"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

type Message = {
  role: "user" | "assistant";
  content: string;
  citations?: { act: string; section: string; text: string }[];
};

const suggestions = [
  "పోలీసులు వారెంట్ లేకుండా అరెస్ట్ చేయవచ్చా?",
  "ఇల్లు అద్దె పెంచవచ్చా? లా ఏమి చెప్పింది?",
  "కంపెనీ జీతం ఇవ్వడం లేదు. ఏమి చేయాలి?",
  "చెక్ బౌన్స్ అయితే ఏమి చేయాలి?",
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "నమస్కారం! 👋 నేను NyayaSathi AI. మీరు ఏమైనా లీగల్ ప్రశ్న అడగండి. నేను తెలుగులో సమాధానం చెప్తాను.\n\n*Disclaimer: ఇది లీగల్ అడ్వైస్ కాదు. విద్యా ప్రయోజనాల కోసం మాత్రమే.*",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/v1/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input, language: "te" }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply,
          citations: data.citations,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "⚠️ సర్వర్ కనెక్ట్ కాలేదు. Backend running లేదేమో చెక్ చేయండి.\n\n`cd backend && uvicorn app.main:app --reload`",
        },
      ]);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-screen">
      <header className="border-b border-zinc-800 px-4 h-14 flex items-center justify-between bg-zinc-950">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl">⚖️</span>
          <span className="font-semibold">NyayaSathi</span>
        </Link>
        <Badge variant="secondary">AI Legal Chat</Badge>
      </header>

      <div className="flex-1 overflow-y-auto px-4 py-4 space-y-4 max-w-3xl mx-auto w-full">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                msg.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-zinc-800 text-zinc-100"
              }`}
            >
              <p className="whitespace-pre-wrap text-sm leading-relaxed">{msg.content}</p>
              {msg.citations && msg.citations.length > 0 && (
                <div className="mt-2 pt-2 border-t border-zinc-700 space-y-1">
                  {msg.citations.map((c, j) => (
                    <p key={j} className="text-xs text-zinc-400">
                      📖 {c.act} — {c.section}
                    </p>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <Card className="bg-zinc-800 px-4 py-3 border-zinc-700">
              <p className="text-sm text-zinc-400">🤔 ఆలోచిస్తున్నాను...</p>
            </Card>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {messages.length === 1 && (
        <div className="px-4 max-w-3xl mx-auto w-full mb-2">
          <p className="text-xs text-zinc-500 mb-2 text-center">Try asking:</p>
          <div className="flex flex-wrap gap-2 justify-center">
            {suggestions.map((s, i) => (
              <button
                key={i}
                onClick={() => {
                  setInput(s);
                }}
                className="text-xs bg-zinc-800 hover:bg-zinc-700 text-zinc-300 px-3 py-1.5 rounded-full transition-colors"
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="border-t border-zinc-800 p-4 bg-zinc-950">
        <div className="max-w-3xl mx-auto flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="మీ లీగల్ ప్రశ్న ఇక్కడ టైప్ చేయండి..."
            className="min-h-[44px] max-h-[120px] bg-zinc-800 border-zinc-700 resize-none"
            rows={1}
          />
          <Button onClick={sendMessage} disabled={loading || !input.trim()} className="px-6">
            {loading ? "..." : "Send"}
          </Button>
        </div>
      </div>
    </div>
  );
}
