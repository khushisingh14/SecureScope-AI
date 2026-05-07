export default function SeverityBadge({ severity }) {
  const label = severity || "Informational";
  const key = label.toLowerCase();
  return <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-bold severity-${key}`}>{label}</span>;
}
