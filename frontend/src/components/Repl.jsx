// frontend/src/Repl.jsx
import { useEffect, useRef, useState } from "react";
import Console from "./console";

export default function Repl({
    apiUrl = "http://127.0.0.1:5000",
    height = 220,
    autoStart = true,
}) {
    const consRef = useRef(null);
    const [sessionId, setSessionId] = useState(null);
    const [logs, setLogs] = useState([]);

    function append(text, type = "out") {
        setLogs((ls) => [...ls, { text: String(text ?? ""), type }]);
    }

    async function ensureSession() {
        if (sessionId) return sessionId;
        const res = await fetch(`${apiUrl}/repl/init`, { method: "POST" });
        const data = await res.json();
        setSessionId(data.session_id);
        append(`Session REPL : ${String(data.session_id).slice(0, 8)}`, "info");
        return data.session_id;
    }

    async function handleSubmit(line) {
        const text = String(line ?? "").trimEnd();
        if (!text) return;
        const sid = await ensureSession();
        append(text, "cmd");
        try {
            const res = await fetch(`${apiUrl}/repl/exec`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sid, line: text }),
            });
            const data = await res.json();
            if (data.output) append(data.output, data.success ? "out" : "err");
        } catch {
            append("Erreur réseau", "err");
        }
    }

    async function handleClear() {
        setLogs([]);
    }

    async function handleCopy(ok) {
        if (ok) append("Copié dans le presse-papiers", "info");
        else append("Échec de copie", "err");
    }

    async function handleReset() {
        if (!sessionId) return;
        try {
            await fetch(`${apiUrl}/repl/reset`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ session_id: sessionId }),
            });
            append("Session réinitialisée", "info");
        } catch {
            append("Erreur de réinitialisation", "err");
        }
    }

    useEffect(() => {
        if (!autoStart) return;
        ensureSession().catch(() => append("Impossible de créer la session", "err"));
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [autoStart]);

    useEffect(() => {
        function onShiftEnter(e) {
            const code = e?.detail?.code;
            if (!code) return;
            const lines = String(code).split("\n").filter((l) => l.trim().length > 0);
            if (!lines.length) return;
            (async () => {
                for (const ln of lines) {
                    // séquence simple ; on pourrait batcher mais on garde ligne par ligne
                    // eslint-disable-next-line no-await-in-loop
                    await handleSubmit(ln);
                }
            })();
        }
        window.addEventListener("editor-shift-enter", onShiftEnter);
        return () => window.removeEventListener("editor-shift-enter", onShiftEnter);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div className="panel full" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <div className="toolbar">
                <span className="badge">REPL</span>
                <div className="spacer" />
                <button className="btn btn-secondary" type="button" onClick={handleReset}>Réinitialiser</button>
            </div>
            <Console
                ref={consRef}
                logs={logs}
                height={height}
                onSubmit={handleSubmit}
                onClear={handleClear}
                onCopy={handleCopy}
                showControls
            />
        </div>
    );
}
