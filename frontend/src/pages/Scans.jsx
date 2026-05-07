import { useEffect, useState } from "react";
import { Download } from "lucide-react";
import api, { asArray, getApiError } from "../api/client";
import UploadDropzone from "../components/UploadDropzone.jsx";
import { downloadReport } from "../utils/downloadReport.js";

export default function Scans() {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(false);
  const [loadingScans, setLoadingScans] = useState(true);
  const [message, setMessage] = useState("");

  const load = async () => {
    try {
      const response = await api.get("/scans");
      setScans(asArray(response.data));
    } catch (err) {
      setScans([]);
      setMessage(getApiError(err, "Could not load scans"));
    } finally {
      setLoadingScans(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const upload = async (form) => {
    setLoading(true);
    setMessage("");
    try {
      // Don't set Content-Type manually - Axios needs to set it with boundary for FormData
      const response = await api.post("/scans/upload", form);
      const findingCount = asArray(response.data?.findings).length;
      setMessage(`Imported ${findingCount} findings from ${response.data?.filename || "scan file"}`);
      await load();
    } catch (err) {
      setMessage(getApiError(err, "Upload failed"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-bold uppercase tracking-[0.28em] text-cyan">Evidence intake</p>
        <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-white">Scan upload and history</h1>
      </div>
      <UploadDropzone onUpload={upload} loading={loading} />
      {message && <p className="rounded-lg border border-line bg-white/[0.03] px-4 py-3 text-sm text-slate-300">{message}</p>}
      {loadingScans && <p className="rounded-lg border border-line bg-white/[0.03] px-4 py-3 text-sm text-slate-300">Loading scans...</p>}
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {scans.map((scan) => (
          <div key={scan.id} className="glass rounded-lg p-5">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-lg font-bold text-white">{scan.name}</p>
                <p className="mt-1 text-sm text-slate-500">{scan.filename}</p>
              </div>
              <span className="rounded-full bg-cyan/10 px-2.5 py-1 text-xs font-bold uppercase text-cyan">{scan.scanner_type}</span>
            </div>
            <div className="mt-5 grid grid-cols-2 gap-3 text-sm">
              <div className="rounded-lg border border-line bg-white/[0.03] p-3">
                <p className="text-slate-500">Findings</p>
                <p className="mt-1 text-xl font-extrabold">{asArray(scan.findings).length}</p>
              </div>
              <div className="rounded-lg border border-line bg-white/[0.03] p-3">
                <p className="text-slate-500">Score</p>
                <p className="mt-1 text-xl font-extrabold">{scan.risk_score}</p>
              </div>
            </div>
            <button onClick={() => downloadReport(scan).catch((err) => setMessage(getApiError(err, "Report download failed")))} className="mt-4 inline-flex items-center gap-2 rounded-lg border border-cyan/30 px-3 py-2 text-sm font-semibold text-cyan hover:bg-cyan/10">
              <Download className="h-4 w-4" />
              Download PDF
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
