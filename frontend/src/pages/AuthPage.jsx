import { useState } from "react";
import { Navigate } from "react-router-dom";
import { motion } from "framer-motion";
import { ShieldCheck } from "lucide-react";
import { useAuth } from "../state/AuthContext.jsx";

export default function AuthPage() {
  const { token, login, register } = useAuth();
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ email: "analyst@securescope.ai", password: "SecureScope123!", full_name: "Security Analyst" });
  const [error, setError] = useState("");

  if (token) return <Navigate to="/" replace />;

  const submit = async (event) => {
    event.preventDefault();
    setError("");
    try {
      if (mode === "login") await login(form.email, form.password);
      else await register(form);
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed");
    }
  };

  return (
    <div className="min-h-screen subtle-grid px-4 py-10">
      <div className="mx-auto grid min-h-[calc(100vh-5rem)] max-w-6xl items-center gap-8 lg:grid-cols-[1.1fr_0.9fr]">
        <motion.section initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center gap-3">
            <div className="grid h-12 w-12 place-items-center rounded-lg border border-cyan/30 bg-cyan/10">
              <ShieldCheck className="h-7 w-7 text-cyan" />
            </div>
            <span className="text-xl font-extrabold">SecureScope AI</span>
          </div>
          <h1 className="mt-10 max-w-3xl text-5xl font-extrabold tracking-tight text-white md:text-7xl">
            AI-powered pentest reporting command center
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-400">
            Import scanner output, normalize evidence, prioritize risk, and generate board-ready cybersecurity assessment reports from one secure workspace.
          </p>
          <div className="mt-8 grid max-w-2xl gap-3 sm:grid-cols-3">
            {["Parser engine", "AI analysis", "PDF reporting"].map((item) => (
              <div key={item} className="rounded-lg border border-line bg-white/[0.03] px-4 py-3 text-sm font-semibold text-slate-300">{item}</div>
            ))}
          </div>
        </motion.section>

        <motion.form initial={{ opacity: 0, x: 16 }} animate={{ opacity: 1, x: 0 }} onSubmit={submit} className="glass rounded-lg p-6">
          <div className="mb-6 grid grid-cols-2 rounded-lg border border-line bg-slate-950/70 p-1">
            {["login", "register"].map((item) => (
              <button
                type="button"
                key={item}
                onClick={() => setMode(item)}
                className={`rounded-md px-4 py-2 text-sm font-bold capitalize ${mode === item ? "bg-cyan text-slate-950" : "text-slate-400"}`}
              >
                {item}
              </button>
            ))}
          </div>

          {mode === "register" && (
            <label className="mb-4 block text-sm text-slate-400">
              Full name
              <input value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} className="mt-2 w-full rounded-lg border border-line bg-slate-950/80 px-3 py-3 text-slate-100 outline-none focus:border-cyan/50" />
            </label>
          )}
          <label className="mb-4 block text-sm text-slate-400">
            Email
            <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} className="mt-2 w-full rounded-lg border border-line bg-slate-950/80 px-3 py-3 text-slate-100 outline-none focus:border-cyan/50" />
          </label>
          <label className="mb-4 block text-sm text-slate-400">
            Password
            <input type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} className="mt-2 w-full rounded-lg border border-line bg-slate-950/80 px-3 py-3 text-slate-100 outline-none focus:border-cyan/50" />
          </label>
          {error && <p className="mb-4 rounded-lg border border-danger/30 bg-danger/10 px-3 py-2 text-sm text-danger">{error}</p>}
          <button className="w-full rounded-lg bg-cyan px-4 py-3 text-sm font-extrabold text-slate-950">
            {mode === "login" ? "Enter workspace" : "Create workspace"}
          </button>
        </motion.form>
      </div>
    </div>
  );
}
