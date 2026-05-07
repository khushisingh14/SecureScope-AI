import { useRef, useState } from "react";
import { UploadCloud } from "lucide-react";

const scannerTypes = [
  { value: "nmap", label: "Nmap XML" },
  { value: "burp", label: "Burp XML" },
  { value: "nikto", label: "Nikto TXT" },
  { value: "sslyze", label: "SSLyze JSON" }
];

export default function UploadDropzone({ onUpload, loading }) {
  const inputRef = useRef(null);
  const [file, setFile] = useState(null);
  const [scanner, setScanner] = useState("nmap");
  const [name, setName] = useState("External Assessment");
  const [scope, setScope] = useState("Internet-facing infrastructure and web application security assessment.");

  const submit = (event) => {
    event.preventDefault();
    if (!file) return;
    const form = new FormData();
    form.append("file", file);
    form.append("scanner_type", scanner);
    form.append("name", name);
    form.append("scope", scope);
    onUpload(form);
  };

  return (
    <form onSubmit={submit} className="glass rounded-lg p-5">
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(event) => event.preventDefault()}
        onDrop={(event) => {
          event.preventDefault();
          setFile(event.dataTransfer.files?.[0]);
        }}
        className="grid cursor-pointer place-items-center rounded-lg border border-dashed border-cyan/35 bg-cyan/[0.04] px-4 py-10 text-center hover:bg-cyan/[0.07]"
      >
        <UploadCloud className="h-10 w-10 text-cyan" />
        <p className="mt-3 font-semibold text-slate-100">{file ? file.name : "Drop a scan file or browse"}</p>
        <p className="mt-1 text-sm text-slate-500">XML, TXT, LOG, and JSON scan exports are validated before parsing.</p>
        <input ref={inputRef} type="file" className="hidden" onChange={(event) => setFile(event.target.files?.[0])} />
      </div>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <label className="text-sm text-slate-400">
          Scan name
          <input value={name} onChange={(e) => setName(e.target.value)} className="mt-2 w-full rounded-lg border border-line bg-slate-950/70 px-3 py-3 text-slate-100 outline-none focus:border-cyan/50" />
        </label>
        <label className="text-sm text-slate-400">
          Scanner
          <select value={scanner} onChange={(e) => setScanner(e.target.value)} className="mt-2 w-full rounded-lg border border-line bg-slate-950/70 px-3 py-3 text-slate-100 outline-none focus:border-cyan/50">
            {scannerTypes.map((type) => <option key={type.value} value={type.value}>{type.label}</option>)}
          </select>
        </label>
      </div>
      <label className="mt-4 block text-sm text-slate-400">
        Scope
        <textarea value={scope} onChange={(e) => setScope(e.target.value)} rows="3" className="mt-2 w-full rounded-lg border border-line bg-slate-950/70 px-3 py-3 text-slate-100 outline-none focus:border-cyan/50" />
      </label>
      <button disabled={!file || loading} className="mt-5 rounded-lg bg-cyan px-5 py-3 text-sm font-extrabold text-slate-950 disabled:cursor-not-allowed disabled:opacity-50">
        {loading ? "Importing scan..." : "Import scan"}
      </button>
    </form>
  );
}
