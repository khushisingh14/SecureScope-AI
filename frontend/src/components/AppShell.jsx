import { NavLink, Outlet } from "react-router-dom";
import { BarChart3, FileDown, LogOut, Radar, Search, ShieldCheck, UploadCloud } from "lucide-react";
import { useAuth } from "../state/AuthContext.jsx";

const nav = [
  { to: "/", label: "Dashboard", icon: BarChart3 },
  { to: "/scans", label: "Scans", icon: UploadCloud },
  { to: "/findings", label: "Findings", icon: Search },
  { to: "/reports", label: "Reports", icon: FileDown }
];

export default function AppShell() {
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen subtle-grid">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-72 border-r border-line bg-slate-950/80 px-5 py-6 backdrop-blur-xl lg:block">
        <div className="flex items-center gap-3">
          <div className="grid h-11 w-11 place-items-center rounded-lg border border-cyan/30 bg-cyan/10">
            <ShieldCheck className="h-6 w-6 text-cyan" />
          </div>
          <div>
            <p className="text-lg font-extrabold tracking-tight">SecureScope AI</p>
            <p className="text-xs uppercase tracking-[0.24em] text-slate-500">Assessment Console</p>
          </div>
        </div>

        <nav className="mt-10 space-y-2">
          {nav.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-3 text-sm font-semibold transition ${
                  isActive ? "bg-cyan/12 text-cyan" : "text-slate-400 hover:bg-white/5 hover:text-slate-100"
                }`
              }
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="absolute bottom-6 left-5 right-5 rounded-lg border border-line bg-white/[0.03] p-4">
          <div className="flex items-center gap-3">
            <div className="grid h-10 w-10 place-items-center rounded-full bg-mint/15 text-sm font-bold text-mint">
              {user?.full_name?.slice(0, 1) || "A"}
            </div>
            <div className="min-w-0">
              <p className="truncate text-sm font-semibold">{user?.full_name || "Analyst"}</p>
              <p className="truncate text-xs text-slate-500">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={logout}
            className="mt-4 flex w-full items-center justify-center gap-2 rounded-lg border border-line px-3 py-2 text-sm text-slate-300 hover:bg-white/5"
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </button>
        </div>
      </aside>

      <main className="lg:pl-72">
        <header className="sticky top-0 z-10 border-b border-line bg-obsidian/70 px-4 py-4 backdrop-blur-xl lg:px-8">
          <div className="flex items-center justify-between gap-4">
            <div className="flex items-center gap-3 lg:hidden">
              <Radar className="h-6 w-6 text-cyan" />
              <span className="font-bold">SecureScope AI</span>
            </div>
            <div className="hidden text-sm text-slate-400 lg:block">Enterprise penetration testing intelligence workspace</div>
            <div className="rounded-full border border-mint/30 bg-mint/10 px-3 py-1 text-xs font-semibold text-mint">Live Assessment</div>
          </div>
        </header>
        <div className="mx-auto max-w-7xl px-4 py-6 lg:px-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
