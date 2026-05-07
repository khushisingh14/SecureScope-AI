import { useEffect, useState } from "react";
import { Download, Sparkles } from "lucide-react";
import api from "../api/client";
import { downloadReport } from "../utils/downloadReport.js";

export default function Reports() {
  const [scans, setScans] = useState([]);
  const [summary, setSummary] = useState("");

  useEffect(() => {
    api.get("/scans").then((response) => setScans(response.data));
  }, []);

  const summarize = async (scan) => {
    setSummary("Generating executive summary...");
    const response = await api.post(`/ai/executive-summary/${scan.id}`);
    setSummary(response.data.summary);
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold uppercase tracking-[0.28em] text-cyan">Deliverables</p>
        <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white">Professional reports</h1>
      </div>
      <div className="grid gap-4 lg:grid-cols-[1fr_0.8fr]">
        <div className="space-y-4">
          {scans.map((scan) => (
            <div key={scan.id} className="glass rounded-lg p-5">
              <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">
                <div>
                  <p className="text-lg font-bold text-white">{scan.name}</p>
                  <p className="mt-1 text-sm text-slate-500">{scan.findings.length} findings | posture score {scan.risk_score}</p>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => summarize(scan)} className="inline-flex items-center gap-2 rounded-lg border border-mint/30 px-3 py-2 text-sm font-semibold text-mint hover:bg-mint/10">
                    <Sparkles className="h-4 w-4" />
                    Summary
                  </button>
                  <button onClick={() => downloadReport(scan)} className="inline-flex items-center gap-2 rounded-lg border border-cyan/30 px-3 py-2 text-sm font-semibold text-cyan hover:bg-cyan/10">
                    <Download className="h-4 w-4" />
                    PDF
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
        <div className="glass rounded-lg p-5">
          <p className="font-bold text-white">Executive summary preview</p>
          <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-400">{summary || "Generate a summary for any scan to preview AI-written report language."}</p>
        </div>
      </div>
    </div>
  );
}
