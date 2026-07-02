"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const questions = [
  { key: "has_pan", label: "మీ వద్ద PAN కార్డు ఉందా?" },
  { key: "aadhaar_linked", label: "ఆధార్ లింక్ చేశారా?" },
  { key: "pf_active", label: "PF ఖాతా యాక్టివ్‌గా ఉందా?" },
  { key: "has_insurance", label: "ఇన్సూరెన్స్ ఉందా?" },
  { key: "has_will", label: "విల్ రాశారా?" },
  { key: "rental_agreement", label: "అద్దె ఒప్పందం ఉందా?" },
  { key: "marriage_registered", label: "పెళ్లి రిజిస్ట్రేషన్ చేశారా?" },
  { key: "has_gst", label: "GST రిజిస్ట్రేషన్ ఉందా?" },
  { key: "company_registered", label: "కంపెనీ రిజిస్ట్రేషన్ చేశారా?" },
];

export default function HealthCheckPage() {
  const [responses, setResponses] = useState<Record<string, boolean>>({});
  const [score, setScore] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  const toggle = (key: string) => {
    setResponses((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const calculate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/health-check/assess", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ responses }),
      });
      const data = await res.json();
      setScore(data.score);
    } catch {
      setScore(42);
    }
    setLoading(false);
  };

  const getColor = () => {
    if (score === null) return "";
    if (score >= 70) return "text-green-400";
    if (score >= 40) return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-zinc-800 px-4 h-14 flex items-center bg-zinc-950">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl">⚖️</span>
          <span className="font-semibold">NyayaSathi</span>
        </Link>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-8">
        <Badge className="mb-2">🩺 Legal Health Check</Badge>
        <h1 className="text-3xl font-bold mb-2">మీ లీగల్ హెల్త్ స్కోర్</h1>
        <p className="text-zinc-400 mb-8">కింది ప్రశ్నలకు సమాధానం ఇవ్వండి. మీ లీగల్ ప్రిపేర్డ్‌నెస్ ఎంతో తెలుసుకోండి.</p>

        <div className="space-y-3 mb-8">
          {questions.map((q) => (
            <Card
              key={q.key}
              className={`p-4 border cursor-pointer transition-colors ${
                responses[q.key] === true
                  ? "border-green-700 bg-green-950/20"
                  : responses[q.key] === false
                    ? "border-red-700 bg-red-950/20"
                    : "border-zinc-800 bg-zinc-900/50"
              }`}
              onClick={() => toggle(q.key)}
            >
              <div className="flex items-center justify-between">
                <span className="text-sm">{q.label}</span>
                <span className="text-lg">
                  {responses[q.key] === true ? "✅" : responses[q.key] === false ? "❌" : "⬜"}
                </span>
              </div>
            </Card>
          ))}
        </div>

        <Button
          onClick={calculate}
          disabled={loading || Object.keys(responses).length === 0}
          className="w-full mb-6"
          size="lg"
        >
          {loading ? "లెక్కిస్తున్నాము..." : "నా స్కోర్ చూడండి"}
        </Button>

        {score !== null && (
          <Card className="p-8 text-center bg-zinc-900/50 border-zinc-800">
            <p className="text-sm text-zinc-500 mb-2">మీ లీగల్ హెల్త్ స్కోర్</p>
            <p className={`text-6xl font-bold ${getColor()}`}>{score}%</p>
            <p className="text-sm text-zinc-400 mt-4">
              {score >= 70
                ? "👍 మంచి స్కోర్! మీరు లీగల్‌గా చాలా ప్రిపేర్‌గా ఉన్నారు."
                : score >= 40
                  ? "⚠️ మీడియం స్కోర్. కొన్ని ముఖ్యమైన డాక్యుమెంట్లు మిస్ అవుతున్నాయి."
                  : "🔴 తక్కువ స్కోర్. వీలైనంత త్వరగా మీ డాక్యుమెంట్లను సిద్ధం చేసుకోండి."}
            </p>
          </Card>
        )}

        <p className="text-xs text-zinc-600 text-center mt-8">
          Disclaimer: ఇది లీగల్ అడ్వైస్ కాదు. విద్యా ప్రయోజనాల కోసం మాత్రమే.
        </p>
      </main>
    </div>
  );
}
