import SeverityBadge from "./SeverityBadge.jsx";

export default function FindingTable({ findings = [], onAnalyze }) {
  const rows = Array.isArray(findings) ? findings.filter(Boolean) : [];

  return (
    <div className="glass overflow-hidden rounded-lg">
      <div className="overflow-x-auto">
        <table className="w-full min-w-[820px] text-left text-sm">
          <thead className="border-b border-line bg-white/[0.03] text-xs uppercase tracking-[0.18em] text-slate-500">
            <tr>
              <th className="px-4 py-3">Finding</th>
              <th className="px-4 py-3">Severity</th>
              <th className="px-4 py-3">Host</th>
              <th className="px-4 py-3">Source</th>
              <th className="px-4 py-3">AI</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {rows.map((finding, index) => (
              <tr key={finding.id ?? `${finding.title}-${index}`} className="hover:bg-white/[0.03]">
                <td className="px-4 py-4">
                  <p className="font-semibold text-slate-100">{finding.title || "Untitled finding"}</p>
                  <p className="mt-1 line-clamp-2 max-w-xl text-xs leading-5 text-slate-500">{finding.description || "No description provided."}</p>
                </td>
                <td className="px-4 py-4"><SeverityBadge severity={finding.severity} /></td>
                <td className="px-4 py-4 font-mono text-xs text-slate-300">{finding.affected_host || "unknown-host"}</td>
                <td className="px-4 py-4 text-slate-400">{finding.source || "Unknown"}</td>
                <td className="px-4 py-4">
                  <button
                    disabled={!finding.id}
                    onClick={() => onAnalyze?.(finding)}
                    className="rounded-lg border border-cyan/30 px-3 py-2 text-xs font-semibold text-cyan hover:bg-cyan/10 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Analyze
                  </button>
                </td>
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td colSpan="5" className="px-4 py-10 text-center text-slate-500">No findings match the current view.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
