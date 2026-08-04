import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "node:path";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    {
      name: "resume-local-print-css",
      transformIndexHtml(html) {
        return html.replace(/(<link rel="stylesheet") crossorigin/gi, "$1");
      },
    },
  ],
  base: "./",
  build: {
    rollupOptions: {
      input: {
        main: resolve(process.cwd(), "index.html"),
        resume: resolve(process.cwd(), "resume/index.html"),
      },
    },
  },
});
