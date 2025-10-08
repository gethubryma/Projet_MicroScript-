import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
    plugins: [react()],
    server: {
        port: 5173,
        proxy: {
            "/run": "http://127.0.0.1:5000",
            "^/repl/.*": "http://127.0.0.1:5000",
            "^/debug/.*": "http://127.0.0.1:5000",
            "/health": "http://127.0.0.1:5000"
        }
    }
});
