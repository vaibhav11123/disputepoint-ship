import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: 5173,
    strictPort: true,
    proxy: {
      "/health": "http://127.0.0.1:8000",
      "/points": "http://127.0.0.1:8000",
      "/rain": "http://127.0.0.1:8000",
      "/replays": "http://127.0.0.1:8000",
      "/evidence": "http://127.0.0.1:8000",
      "/meta": "http://127.0.0.1:8000",
    },
  },
});
