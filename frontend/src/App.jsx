
import { useEffect, useRef, useState } from "react";
import Editor from "./components/Editor.jsx";
import Repl from "./components/Repl.jsx";
import VariableInspector from "./components/VariableInspector.jsx";

const API_URL = "http://127.0.0.1:5000";

export default function App() {
    const editorRef = useRef(null);

    const [statusText, setStatusText] = useState("Prêt");
    const [statusError, setStatusError] = useState(false);

    const [breakpoints, setBreakpoints] = useState([]);
    const [output, setOutput] = useState("(aucune sortie)");
    const [dbgSid, setDbgSid] = useState(null);
    const [variables, setVariables] = useState({});
    const [callstack, setCallstack] = useState([]);

    async function postJSON(url, body, timeout = 15000) {
        const controller = new AbortController();
        const t = setTimeout(() => controller.abort(), timeout);
        try {
            const res = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
                signal: controller.signal
            });
            const data = await res.json().catch(() => ({}));
            return { ok: res.ok, data };
        } finally {
            clearTimeout(t);
        }
    }

    async function run(code) {
        setStatusError(false);
        setStatusText("Exécution…");
        setOutput("Exécution…");
        const { ok, data } = await postJSON(`${API_URL}/run`, { code }).catch(() => ({ ok: false, data: { success: false, output: "Erreur de connexion." } }));
        setOutput(data.output || "(aucune sortie)");
        setStatusError(!data.success || !ok);
        setStatusText(ok ? "Terminé" : "Erreur");
    }

    async function runTimed(code) {
        const t0 = performance.now();
        await run(code);
        const t1 = performance.now();
        setOutput((prev) => `${prev}\n\n⏱ ${Math.max(0, t1 - t0).toFixed(1)} ms`);
    }

    function handleFormat() {
        editorRef.current?.format?.();
    }

    async function debugStart() {
        const code = editorRef.current?.getValue?.() ?? "";
        setStatusText("Debug…");
        const { ok, data } = await postJSON(`${API_URL}/debug/start`, { code, breakpoints }).catch(() => ({ ok: false, data: { error: "Erreur debug/start" } }));
        if (!ok || data.error) {
            setStatusError(true);
            setStatusText("Erreur debug");
            return;
        }
        setDbgSid(data.session_id);
        setStatusError(false);
        setStatusText("En pause");
        await refreshDebugState(data.session_id);
    }

    async function debugStep() {
        if (!dbgSid) return;
        setStatusText("Step…");
        const { ok, data } = await postJSON(`${API_URL}/debug/step`, { session_id: dbgSid }).catch(() => ({ ok: false, data: { error: "Erreur debug/step" } }));
        if (!ok || data.error) {
            setStatusError(true);
            setStatusText("Erreur step");
            return;
        }
        await refreshDebugState(dbgSid);
    }

    async function debugContinue() {
        if (!dbgSid) return;
        setStatusText("Continue…");
        const { ok, data } = await postJSON(`${API_URL}/debug/continue`, { session_id: dbgSid }).catch(() => ({ ok: false, data: { error: "Erreur debug/continue" } }));
        if (!ok || data.error) {
            setStatusError(true);
            setStatusText("Erreur continue");
            return;
        }
        await refreshDebugState(dbgSid);
    }

    async function debugSetBreakpoints(lines) {
        setBreakpoints(lines);
        if (!dbgSid) return;
        await postJSON(`${API_URL}/debug/set_breakpoints`, { session_id: dbgSid, breakpoints: lines }).catch(() => null);
        await refreshDebugState(dbgSid);
    }

    async function refreshDebugState(sid = dbgSid) {
        if (!sid) return;
        const url = new URL(`${API_URL}/debug/state`);
        url.searchParams.set("session_id", sid);
        try {
            const res = await fetch(url.toString());
            const js = await res.json();
            if (js.error) throw new Error(js.error);
            const st = js.state || {};
            setVariables(st.variables || {});
            setCallstack(st.callstack || []);
            setStatusError(!!st.error);
            setStatusText(st.paused ? "En pause" : "Terminé");
        } catch {
            setStatusError(true);
            setStatusText("Erreur état");
        }
    }

    function handleRunClick() {
        const code = editorRef.current?.getValue?.() ?? "";
        run(code);
    }

    function handleRunTimedClick() {
        const code = editorRef.current?.getValue?.() ?? "";
        runTimed(code);
    }

    function handleEditorChange() {
        setStatusText("Modifié");
        setStatusError(false);
    }

    function handleToggleBreakpoint(_line, all) {
        debugSetBreakpoints(all);
    }

    useEffect(() => {
        const t = setInterval(() => {
            if (dbgSid) refreshDebugState();
        }, 1500);
        return () => clearInterval(t);
    }, [dbgSid]);

    return (
        <div className="app">
            <header>
                <h1>MicroScript IDE</h1>
                <div className="actions">
                    <button id="run-btn" onClick={handleRunClick}>Exécuter</button>
                    <button id="format-btn" title="Simple indentation" onClick={handleFormat}>✨</button>
                    <button id="run-timed" className="btn btn-secondary" onClick={handleRunTimedClick}>⏱ Exécuter</button>
                </div>
            </header>

            <div className="toolbar mt-8">
                <span className="badge">Outils</span>
                <button className="btn" onClick={debugStart}>Debug</button>
                <button className="btn btn-secondary" onClick={debugStep}>Step</button>
                <button className="btn btn-secondary" onClick={debugContinue}>Continue</button>
                <div className="spacer"></div>
                <div className="statusbar">
                    <span className={`dot${statusError ? " err" : ""}`} aria-hidden="true"></span>
                    <span id="status-text">{statusText}</span>
                </div>
            </div>

            <main className="grid">
                <section className="panel">
                    <h2>Éditeur</h2>
                    <Editor
                        ref={editorRef}
                        initialValue={`x = 10\ny = x + 5\nprint(y)\nif y > 10:\n    print(y)`}
                        mode="python"
                        height={360}
                        breakpoints={breakpoints}
                        onChange={handleEditorChange}
                        onRun={(code) => run(code)}
                        onRunTimed={(code) => runTimed(code)}
                        onFormat={handleFormat}
                        onToggleBreakpoint={handleToggleBreakpoint}
                    />
                </section>

                <section className="panel">
                    <h2>Sortie</h2>
                    <pre id="output" className="terminal" aria-live="polite">{output}</pre>
                </section>

                <section className="panel full">
                    <Repl apiUrl={API_URL} height={220} autoStart />
                </section>

                <section className="panel">
                    <VariableInspector
                        title="Variables"
                        variables={variables}
                        onRefresh={() => refreshDebugState()}
                    />
                </section>

                <section className="panel">
                    <h2>Pile d’appels</h2>
                    <div id="callstack-list" className="inspector">
                        {(!callstack || callstack.length === 0) ? (
                            <div className="text-dim">Pile vide.</div>
                        ) : (
                            callstack.map((f, i) => (
                                <div key={i} className="card">
                                    <h3>#{i} {f.function || "(?)"}</h3>
                                    <div className="kv">
                                        <span className="text-dim">fichier</span>
                                        <span>{String(f.filename || "")}</span>
                                    </div>
                                    <div className="kv">
                                        <span className="text-dim">ligne</span>
                                        <span>{String(f.line || "")}</span>
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </section>
            </main>
        </div>
    );
}
