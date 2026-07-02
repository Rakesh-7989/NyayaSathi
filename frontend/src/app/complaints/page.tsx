"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

const complaintTypes = [
  { id: "consumer", label: "🛒 వినియోగదారుల ఫిర్యాదు", desc: "కొనుగోలు చేసిన ఉత్పత్తి/సేవపై ఫిర్యాదు" },
  { id: "police", label: "🚔 పోలీసు ఫిర్యాదు", desc: "నేరం, దొంగతనం, వేధింపులపై ఫిర్యాదు" },
  { id: "legal_notice", label: "⚖️ చట్టపరమైన నోటీసు", desc: "వ్యక్తి/కంపెనీకి లీగల్ నోటీసు" },
  { id: "rti", label: "📋 RTI దరఖాస్తు", desc: "ప్రభుత్వ సమాచారం కోసం దరఖాస్తు" },
  { id: "cyber_crime", label: "💻 సైబర్ నేర ఫిర్యాదు", desc: "ఆన్‌లైన్ మోసం, హ్యాకింగ్, సోషల్ మీడియా వేధింపులు" },
  { id: "labour", label: "👷 లేబర్ ఫిర్యాదు", desc: "జీతం, PF, ESI, ఉద్యోగ సమస్యలు" },
];

export default function ComplaintsPage() {
  const [selectedType, setSelectedType] = useState(complaintTypes[0]);
  const [details, setDetails] = useState("నేను కొనుగోలు చేసిన ఉత్పత్తిలో లోపాలు ఉన్నాయి. కంపెనీ రీఫండ్ ఇవ్వడం లేదు.");
  const [generated, setGenerated] = useState("");
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/v1/complaints/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          complaint_type: selectedType.id,
          details: {
            name: "మీ పేరు",
            address: "మీ చిరునామా",
            complaint_description: details,
            product_or_service: "ఉత్పత్తి/సేవ",
            date_of_purchase: "01-01-2026",
            incident_description: details,
            incident_date: "01-01-2026",
            incident_place: "స్థలం",
            sender_name: "మీ పేరు",
            sender_address: "మీ చిరునామా",
            lawyer_name: "న్యాయవాది పేరు",
            recipient_name: "గ్రహీత పేరు",
            notice_description: details,
            deadline_days: "30",
            demand: "చెల్లింపు",
            information_requested: details,
            timeframe: "30",
            company_name: "కంపెనీ పేరు",
            designation: "హోదా",
          },
          language: "te",
        }),
      });
      const data = await res.json();
      setGenerated(data.complaint);
    } catch {
      setGenerated(`⚠️ సర్వర్ కనెక్ట్ కాలేదు. డెమో మోడ్.\n\n---\n\nతేదీ: 02-07-2026\n\nగౌరవనీయ అధికారులకు,\n\n${details}\n\nదయచేసి తగిన చర్యలు తీసుకోవాల్సిందిగా విన్నవించుకుంటున్నాను.\n\n- మీ పేరు`);
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
        <Badge className="mb-2">📝 Complaint Generator</Badge>
        <h1 className="text-3xl font-bold mb-2">ఫిర్యాదు ఉత్పత్తి</h1>
        <p className="text-zinc-400 mb-8">మీ కేసుకు తగిన కంప్లయింట్ టెంప్లేట్ సెలక్ట్ చేసి, వివరాలు నింపండి.</p>

        <div className="grid grid-cols-2 md:grid-cols-3 gap-2 mb-8">
          {complaintTypes.map((ct) => (
            <Card
              key={ct.id}
              className={`p-3 cursor-pointer transition-colors ${
                selectedType.id === ct.id
                  ? "border-primary bg-primary/10"
                  : "border-zinc-800 bg-zinc-900/50 hover:bg-zinc-800"
              }`}
              onClick={() => { setSelectedType(ct); setGenerated(""); }}
            >
              <p className="text-sm font-medium">{ct.label}</p>
              <p className="text-xs text-zinc-500 mt-1">{ct.desc}</p>
            </Card>
          ))}
        </div>

        <Card className="p-6 bg-zinc-900/50 border-zinc-800 mb-6">
          <h3 className="font-medium mb-3">{selectedType.label} — వివరాలు నమోదు చేయండి</h3>
          <Textarea
            value={details}
            onChange={(e) => setDetails(e.target.value)}
            className="min-h-[120px] bg-zinc-800 border-zinc-700 mb-4"
            placeholder="మీ సమస్యను వివరించండి..."
          />
          <Button onClick={generate} disabled={loading || !details.trim()} className="w-full">
            {loading ? "ఉత్పత్తి చేస్తున్నాము..." : "📄 కంప్లయింట్ జనరేట్ చేయండి"}
          </Button>
        </Card>

        {generated && (
          <Card className="p-6 bg-zinc-900/50 border-zinc-800">
            <div className="flex justify-between items-center mb-4">
              <h3 className="font-semibold">✅ జనరేటెడ్ కంప్లయింట్</h3>
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigator.clipboard.writeText(generated)}
              >
                📋 కాపీ
              </Button>
            </div>
            <div className="bg-zinc-950 p-4 rounded-lg whitespace-pre-wrap text-sm text-zinc-300 font-mono leading-relaxed">
              {generated}
            </div>
          </Card>
        )}
      </main>
    </div>
  );
}
