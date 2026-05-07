import { useEffect, useState } from "react";
import { AlertTriangle, FileSearch, Radar, ShieldCheck } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import api, { asArray, getApiError } from "../api/client";
import FindingTable from "../components/FindingTable.jsx";
import RiskMeter from "../components/RiskMeter.jsx";
import StatCard from "../components/StatCard.jsx";
import UploadDropzone from "../components/UploadDropzone.jsx";

const severityColors = {
  Critical: "#FB7185",
  High: "#F59E0B",
  Medium: "#FDE047",
  Low: "#22D3EE",
  Informational: "#34D399"
};

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [findings, setFindings] = useState([]);
  const [analysis, setAnalysis] = useState("");
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const load = async () => {
    setError("");
    try {
      const [dashboard, findingList] = await Promise.all([api.get("/dashboard"), api.get("/findings?sort=severity&direction=desc")]);
      setStats(dashboard.data && typeof dashboard.data === "object" ? dashboard.data : null);
      setFindings(asArray(findingList.data).slice(0, 8));
    } catch (err) {
      setError(getApiError(err, "Could not load dashboard data"));
      setStats(null);
      setFindings([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const analyze = async (finding) => {
    setAnalysis("Generating AI analyst note...");
    try {
      const response = await api.post("/ai/analyze", { finding_id: finding.id });
      setAnalysis(response.data?.analysis || "No analysis was returned.");
    } catch (err) {
      setAnalysis(getApiError(err, "AI analysis failed"));
    }
  };

  const upload = async (form) => {
    setUploading(true);
    setMessage("");
    try {
      const response = await api.post("/scans/upload", form);
      const count = asArray(response.data?.findings).length;
      setMessage(`Imported ${count} findings from ${response.data?.filename || "scan file"}`);
      await load();
    } catch (err) {
      setMessage(getApiError(err, "Upload failed"));
    } finally {
      setUploading(false);
    }
  };

  const severityData = Object.entries(stats?.severity_counts || {}).map(([name, value]) => ({ name, value }));
  const sourceData = Object.entries(stats?.source_counts || {}).map(([name, value]) => ({ name, value }));

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
        <div>
          <p className="text-sm font-bold uppercase tracking-[0.28em] text-cyan">Assessment overview</p>
          <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white md:text-4xl">Security posture dashboard</h1>
        </div>
      </div>
      {error && <p className="rounded-lg border border-danger/25 bg-danger/10 px-4 py-3 text-sm text-rose-200">{error}</p>}
      {loading && <p className="rounded-lg border border-line bg-white/[0.03] px-4 py-3 text-sm text-slate-300">Loading dashboard data...</p>}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <StatCard title="Scans imported" value={stats?.scan_count ?? 0} detail="Historical scanner evidence" icon={Radar} tone="cyan" />
        <StatCard title="Findings" value={stats?.finding_count ?? 0} detail="Normalized vulnerabilities" icon={FileSearch} tone="amber" />
        <StatCard title="Posture score" value={stats?.posture_score ?? 100} detail="Weighted by severity" icon={ShieldCheck} tone="mint" />
        <StatCard title="Critical/High" value={(stats?.severity_counts?.Critical ?? 0) + (stats?.severity_counts?.High ?? 0)} detail="Needs rapid triage" icon={AlertTriangle} tone="danger" />
      </div>

      <UploadDropzone onUpload={upload} loading={uploading} />
      {message && <p className="rounded-lg border border-line bg-white/[0.03] px-4 py-3 text-sm text-slate-300">{message}</p>}

      <div className="grid gap-6 xl:grid-cols-[0.8fr_1.2fr]">
        <RiskMeter score={stats?.posture_score ?? 100} />
        <div className="glass rounded-lg p-5">
          <div className="mb-5 flex items-center justify-between">
            <p className="font-bold text-white">Severity distribution</p>
            <span className="text-xs text-slate-500">Weighted risk mix</span>
          </div>
          <div className="h-72">
            <ResponsiveContainer>
              <BarChart data={severityData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.12)" />
                <XAxis dataKey="name" stroke="#64748B" fontSize={12} />
                <YAxis stroke="#64748B" fontSize={12} />
                <Tooltip contentStyle={{ background: "#0F172A", border: "1px solid rgba(148,163,184,0.18)", borderRadius: 8 }} />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {severityData.map((entry) => <Cell key={entry.name} fill={severityColors[entry.name]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
        <div>
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-xl font-extrabold text-white">Priority findings</h2>
          </div>
          <FindingTable findings={findings} onAnalyze={analyze} />
        </div>
        <div className="space-y-6">
          <div className="glass rounded-lg p-5">
            <p className="mb-5 font-bold text-white">Scanner coverage</p>
            <div className="h-56">
              <ResponsiveContainer>
                <PieChart>
                  <Pie data={sourceData} dataKey="value" nameKey="name" innerRadius={52} outerRadius={78} paddingAngle={4}>
                    {sourceData.map((entry, index) => <Cell key={entry.name} fill={["#22D3EE", "#34D399", "#F59E0B", "#FB7185"][index % 4]} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: "#0F172A", border: "1px solid rgba(148,163,184,0.18)", borderRadius: 8 }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>
          <div className="glass rounded-lg p-5">
            <p className="font-bold text-white">AI analyst note</p>
            <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-400">{analysis || "Select Analyze on a finding to generate remediation context and prioritization."}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
