"use client";

import { useState, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

export default function DocumentsPage() {
  const [file, setFile] = useState<File | null>(null);
  const [analysis, setAnalysis] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f && (f.type.includes("pdf") || f.type.includes("image") || f.type.includes("text"))) {
      setFile(f);
    }
  };

  const upload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      const res = await fetch("http://localhost:8000/api/v1/documents/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setAnalysis(data.analysis);
    } catch {
      setAnalysis({
        summary: "⚠️ సర్వర్ కనెక్ట్ కాలేదు. ప్రస్తుతం డెమో మోడ్‌లో ఉంది.",
        risks: ["డాక్యుమెంట్ లో లీగల్ రిస్క్‌లు ఉండవచ్చు", "షరతులు స్పష్టంగా లేవు"],
        missing_clauses: ["మెయింటెనెన్స్ క్లాజ్ లేదు", "వివాద పరిష్కార క్లాజ్ లేదు"],
        suggestions: ["న్యాయ నిపుణులకు చూపించండి", "సాధారణ భాషలో రాయించండి"],
      });
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-zinc-800 px-4 h-14 flex items-center bg-zinc-950">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl">⚖️</span>
          <span className="font-semibold">NyayaSathi</span>
        </Link>
      </header>

      <main className="max-w-3xl mx-auto px-4 py-8">
        <Badge className="mb-2">📄 Document Analysis</Badge>
        <h1 className="text-3xl font-bold mb-2">మీ డాక్యుమెంట్‌ను అనలైజ్ చేయండి</h1>
        <p className="text-zinc-400 mb-8">Notice, Agreement, Court Order, Rental Agreement, Offer Letter లను అప్‌లోడ్ చేయండి. AI రిస్క్‌లు, మిస్సింగ్ క్లాజ్‌లు మరియు సూచనలు తెలియజేస్తుంది.</p>

        <Card
          className={`p-12 border-2 border-dashed text-center cursor-pointer transition-colors mb-6 ${
            dragOver ? "border-primary bg-primary/5" : "border-zinc-700 bg-zinc-900/50"
          }`}
          onDrop={handleDrop}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onClick={() => inputRef.current?.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf,.doc,.docx,.txt,.png,.jpg,.jpeg"
            className="hidden"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
          <div className="text-5xl mb-4">📄</div>
          {file ? (
            <div>
              <p className="font-medium">{file.name}</p>
              <p className="text-sm text-zinc-500">{(file.size / 1024).toFixed(1)} KB</p>
              <Button size="sm" className="mt-4" onClick={(e) => { e.stopPropagation(); upload(); }} disabled={loading}>
                {loading ? "అనలైజ్ చేస్తున్నాము..." : "అనలైజ్ చేయండి"}
              </Button>
            </div>
          ) : (
            <p className="text-zinc-400">PDF, DOCX, Image ఫైల్‌ను డ్రాగ్ చేయండి లేదా క్లిక్ చేసి ఎంచుకోండి</p>
          )}
        </Card>

        {analysis && (
          <div className="space-y-4">
            <Card className="p-6 bg-zinc-900/50 border-zinc-800">
              <h3 className="font-semibold mb-3">📋 సారాంశం</h3>
              <p className="text-zinc-300">{analysis.summary}</p>
            </Card>

            {analysis.risks?.length > 0 && (
              <Card className="p-6 bg-red-950/20 border-red-900/50">
                <h3 className="font-semibold mb-3 text-red-400">⚠️ రిస్క్‌లు</h3>
                <ul className="space-y-2">
                  {analysis.risks.map((r: string, i: number) => (
                    <li key={i} className="text-sm text-zinc-300 flex items-start gap-2">
                      <span>•</span> {r}
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {analysis.missing_clauses?.length > 0 && (
              <Card className="p-6 bg-yellow-950/20 border-yellow-900/50">
                <h3 className="font-semibold mb-3 text-yellow-400">📌 మిస్సింగ్ క్లాజ్‌లు</h3>
                <ul className="space-y-2">
                  {analysis.missing_clauses.map((m: string, i: number) => (
                    <li key={i} className="text-sm text-zinc-300 flex items-start gap-2">
                      <span>•</span> {m}
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {analysis.suggestions?.length > 0 && (
              <Card className="p-6 bg-green-950/20 border-green-900/50">
                <h3 className="font-semibold mb-3 text-green-400">💡 సూచనలు</h3>
                <ul className="space-y-2">
                  {analysis.suggestions.map((s: string, i: number) => (
                    <li key={i} className="text-sm text-zinc-300 flex items-start gap-2">
                      <span>→</span> {s}
                    </li>
                  ))}
                </ul>
              </Card>
            )}
          </div>
        )}

        <p className="text-xs text-zinc-600 text-center mt-8">
          Disclaimer: ఇది లీగల్ అడ్వైస్ కాదు. విద్యా ప్రయోజనాల కోసం మాత్రమే.
        </p>
      </main>
    </div>
  );
}
