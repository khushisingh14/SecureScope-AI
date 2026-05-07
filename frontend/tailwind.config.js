/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        obsidian: "#070B12",
        panel: "rgba(15, 23, 42, 0.74)",
        line: "rgba(148, 163, 184, 0.18)",
        cyan: "#22D3EE",
        mint: "#34D399",
        amber: "#F59E0B",
        danger: "#FB7185"
      },
      boxShadow: {
        glow: "0 0 40px rgba(34, 211, 238, 0.12)"
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};
