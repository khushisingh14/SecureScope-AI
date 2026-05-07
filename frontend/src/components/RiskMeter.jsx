export default function RiskMeter({ score = 100 }) {
  const normalized = Math.max(0, Math.min(100, Number(score) || 0));
  const color = normalized >= 80 ? "#34D399" : normalized >= 55 ? "#F59E0B" : "#FB7185";

  return (
    <div className="glass rounded-lg p-5">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">Security posture</p>
          <p className="mt-2 text-4xl font-extrabold text-white">{normalized}</p>
        </div>
        <div
          className="grid h-28 w-28 place-items-center rounded-full"
          style={{ background: `conic-gradient(${color} ${normalized * 3.6}deg, rgba(148, 163, 184, 0.16) 0deg)` }}
        >
          <div className="grid h-20 w-20 place-items-center rounded-full bg-slate-950 text-sm font-bold" style={{ color }}>
            {normalized >= 80 ? "Strong" : normalized >= 55 ? "Watch" : "Risk"}
          </div>
        </div>
      </div>
      <div className="mt-5 h-2 rounded-full bg-slate-800">
        <div className="h-2 rounded-full" style={{ width: `${normalized}%`, background: color }} />
      </div>
    </div>
  );
}
