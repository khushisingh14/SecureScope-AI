export default function SeverityBadge({ severity }) {
  const key = (severity || "Informational").toLowerCase();
  return <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-bold severity-${key}`}>{severity}</span>;
}
