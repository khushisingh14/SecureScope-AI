import { useEffect, useState } from "react";
import api from "../api/client";
import FindingTable from "../components/FindingTable.jsx";

export default function Findings() {
  const [findings, setFindings] = useState([]);
  const [filters, setFilters] = useState({ search: "", severity: "", source: "", direction: "desc" });
  const [analysis, setAnalysis] = useState("");

  const load = async () => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => value && params.append(key, value));
    params.append("sort", "severity");
    const response = await api.get(`/findings?${params.toString()}`);
    setFindings(response.data);
  };

  useEffect(() => {
    load();
  }, [filters]);

  const analyze = async (finding) => {
    setAnalysis("Generating AI analyst note...");
    const response = await api.post("/ai/analyze", { finding_id: finding.id });
    setAnalysis(response.data.analysis);
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold uppercase tracking-[0.28em] text-cyan">Risk register</p>
        <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white">Findings triage</h1>
      </div>
      <div className="glass grid gap-3 rounded-lg p-4 md:grid-cols-4">
        <input placeholder="Search findings" value={filters.search} onChange={(e) => setFilters({ ...filters, search: e.target.value })} className="rounded-lg border border-line bg-slate-950/70 px-3 py-3 text-sm outline-none focus:border-cyan/50 md:col-span-2" />
        <select value={filters.severity} onChange={(e) => setFilters({ ...filters, severity: e.target.value })} className="rounded-lg border border-line bg-slate-950/70 px-3 py-3 text-sm outline-none focus:border-cyan/50">
          <option value="">All severities</option>
          {["Critical", "High", "Medium", "Low", "Informational"].map((item) => <option key={item}>{item}</option>)}
        </select>
        <select value={filters.direction} onChange={(e) => setFilters({ ...filters, direction: e.target.value })} className="rounded-lg border border-line bg-slate-950/70 px-3 py-3 text-sm outline-none focus:border-cyan/50">
          <option value="desc">Highest first</option>
          <option value="asc">Lowest first</option>
        </select>
      </div>
      <FindingTable findings={findings} onAnalyze={analyze} />
      {analysis && <div className="glass rounded-lg p-5"><p className="font-bold text-white">AI analysis</p><p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-400">{analysis}</p></div>}
    </div>
  );
}
