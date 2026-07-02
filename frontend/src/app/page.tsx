"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const features = [
  {
    title: "💬 AI Legal Chat",
    desc: "Ask any legal question in Telugu, Hindi, or English. Get answers with sections and citations.",
  },
  {
    title: "📄 Document Analysis",
    desc: "Upload notices, agreements, or court orders. AI explains risks and missing clauses.",
  },
  {
    title: "🩺 Legal Health Check",
    desc: "Score your legal preparedness. Know what documents you're missing.",
  },
  {
    title: "📝 Complaint Generator",
    desc: "Generate consumer complaints, legal notices, RTI, and police complaints instantly.",
  },
  {
    title: "🎙 Voice Assistant",
    desc: "Speak your question in Telugu. Get spoken answers back.",
  },
  {
    title: "⚖️ Know Your Rights",
    desc: "One-tap guidance for police stops, salary delays, cyber fraud & more.",
  },
];

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <header className="border-b border-zinc-800">
        <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">⚖️</span>
            <span className="font-bold text-xl">NyayaSathi</span>
            <Badge variant="secondary" className="ml-2">MVP</Badge>
          </div>
          <div className="flex items-center gap-1">
            <Link href="/chat"><Button variant="ghost" size="sm">Chat</Button></Link>
            <Link href="/health-check"><Button variant="ghost" size="sm">Health</Button></Link>
            <Link href="/documents"><Button variant="ghost" size="sm">Docs</Button></Link>
            <Link href="/complaints"><Button variant="ghost" size="sm">Complaints</Button></Link>
            <Link href="/chat"><Button size="sm" className="ml-2">Get Started</Button></Link>
          </div>
        </div>
      </header>

      <main className="flex-1">
        <section className="max-w-6xl mx-auto px-4 py-20 text-center">
          <Badge className="mb-4" variant="secondary">AI Legal Companion</Badge>
          <h1 className="text-5xl font-bold tracking-tight mb-4">
            Know Your Rights
            <br />
            <span className="text-zinc-500">Before You Need a Lawyer</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mx-auto mb-8">
            India&apos;s first AI Legal Operating System. Understand your legal rights,
            analyze documents, and generate complaints — all in your own language.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/chat">
              <Button size="lg" className="text-base">Ask a Legal Question</Button>
            </Link>
            <Link href="/health-check">
              <Button size="lg" variant="outline" className="text-base">Check Legal Health</Button>
            </Link>
          </div>
        </section>

        <section className="max-w-6xl mx-auto px-4 py-16">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {features.map((f) => (
              <Card key={f.title} className="p-6 bg-zinc-900/50 border-zinc-800">
                <h3 className="font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-sm text-zinc-400">{f.desc}</p>
              </Card>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t border-zinc-800 py-8 text-center text-sm text-zinc-600">
        <p>NyayaSathi — Not legal advice. For educational purposes only.</p>
      </footer>
    </div>
  );
}
