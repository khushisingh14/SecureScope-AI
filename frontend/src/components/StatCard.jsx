import { motion } from "framer-motion";

export default function StatCard({ title, value, detail, icon: Icon, tone = "cyan" }) {
  const tones = {
    cyan: "text-cyan bg-cyan/10 border-cyan/20",
    mint: "text-mint bg-mint/10 border-mint/20",
    amber: "text-amber bg-amber/10 border-amber/20",
    danger: "text-danger bg-danger/10 border-danger/20"
  };

  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-lg p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-slate-400">{title}</p>
          <p className="mt-2 text-3xl font-extrabold tracking-tight text-white">{value}</p>
        </div>
        <div className={`grid h-11 w-11 place-items-center rounded-lg border ${tones[tone]}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      <p className="mt-4 text-sm text-slate-500">{detail}</p>
    </motion.div>
  );
}
