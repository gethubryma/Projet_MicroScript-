const API_URL = "http://127.0.0.1:5000";

const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    mode: "python",
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4
});
editor.setValue(`x = 10
y = x + 5
print(y)
if y > 10:
    print(y)`);

const output = document.getElementById("output");
const log = document.getElementById("repl-log");
const lineInput = document.getElementById("repl-line");

document.getElementById("run-btn").addEventListener("click", async () => {
    const code = editor.getValue();
    output.textContent = "Exécution...";
    try {
        const res = await fetch(`${API_URL}/run`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code })
        });
        const data = await res.json();
        output.classList.toggle("err", !data.success);
        output.textContent = data.output || "(aucune sortie)";
    } catch (e) {
        output.classList.add("err");
        output.textContent = "Erreur de connexion au serveur.";
    }
});

document.getElementById("format-btn").addEventListener("click", () => {
    const txt = editor.getValue().split("\n").map(s => s.replace(/\t/g, "    ")).join("\n");
    editor.setValue(txt);
});

let SESSION_ID = null;

async function ensureReplSession() {
    if (SESSION_ID) return SESSION_ID;
    const res = await fetch(`${API_URL}/repl/init`, { method: "POST" });
    const data = await res.json();
    SESSION_ID = data.session_id;
    log.insertAdjacentHTML("beforeend", `<div>Session REPL : <b>${SESSION_ID.slice(0, 8)}</b></div>`);
    return SESSION_ID;
}

async function replExec() {
    const text = lineInput.value;
    if (!text.trim()) return;
    await ensureReplSession();
    log.insertAdjacentHTML("beforeend", `<div><span>&gt;&gt;&gt;</span> ${text}</div>`);
    lineInput.value = "";
    try {
        const res = await fetch(`${API_URL}/repl/exec`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: SESSION_ID, line: text })
        });
        const data = await res.json();
        const cls = data.success ? "" : "err";
        if (data.output) {
            log.insertAdjacentHTML("beforeend", `<div class="${cls}">${escapeHtml(data.output)}</div>`);
        }
    } catch (e) {
        log.insertAdjacentHTML("beforeend", `<div class="err"> Erreur réseau</div>`);
    }
    log.scrollTop = log.scrollHeight;
}

function escapeHtml(s) { return s.replace(/[&<>]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c])); }

document.getElementById("repl-run").addEventListener("click", replExec);
lineInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") replExec();
});

document.getElementById("repl-reset").addEventListener("click", async () => {
    if (!SESSION_ID) return;
    await fetch(`${API_URL}/repl/reset`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: SESSION_ID })
    });
    log.insertAdjacentHTML("beforeend", `<div> Session réinitialisée</div>`);
});

async function postJSON(url, body, opts = {}) {
    const controller = new AbortController();
    const t = setTimeout(() => controller.abort(), opts.timeout ?? 8000);
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

const LS_KEY = "microscript.editor";
try {
    const saved = localStorage.getItem(LS_KEY);
    if (saved && saved.length > 0) editor.setValue(saved);
} catch (_) { }
let saveTimer;
editor.on("change", () => {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
        try { localStorage.setItem(LS_KEY, editor.getValue()); } catch (_) { }
    }, 300);
});

document.addEventListener("keydown", (e) => {
    const isMac = navigator.platform.toUpperCase().includes("MAC");
    const mod = isMac ? e.metaKey : e.ctrlKey;
    if (mod && e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        document.getElementById("run-btn").click();
    }
    if (!mod && e.key === "Enter" && e.shiftKey) {
        e.preventDefault();
        replExec();
    }
    if (mod && (e.key.toLowerCase() === "s")) {
        e.preventDefault();
        try { localStorage.setItem(LS_KEY, editor.getValue()); } catch (_) { }
    }
});

async function runWithTiming() {
    const code = editor.getValue();
    const t0 = performance.now();
    output.textContent = "Exécution...";
    const { ok, data } = await postJSON(`${API_URL}/run`, { code }, { timeout: 15000 }).catch(() => ({ ok: false, data: { success: false, output: "Erreur de connexion." } }));
    const t1 = performance.now();
    output.classList.toggle("err", !data.success);
    const suffix = `\n\n⏱ ${Math.max(0, (t1 - t0)).toFixed(1)} ms`;
    output.textContent = (data.output || "(aucune sortie)") + suffix;
}

const replHistory = [];
let replIndex = -1;
lineInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        if (lineInput.value.trim()) {
            replHistory.push(lineInput.value);
            replIndex = replHistory.length;
        }
    } else if (e.key === "ArrowUp") {
        if (replHistory.length) {
            replIndex = Math.max(0, replIndex - 1);
            lineInput.value = replHistory[replIndex] || "";
            setTimeout(() => lineInput.setSelectionRange(lineInput.value.length, lineInput.value.length), 0);
            e.preventDefault();
        }
    } else if (e.key === "ArrowDown") {
        if (replHistory.length) {
            replIndex = Math.min(replHistory.length, replIndex + 1);
            lineInput.value = replHistory[replIndex] || "";
            setTimeout(() => lineInput.setSelectionRange(lineInput.value.length, lineInput.value.length), 0);
            e.preventDefault();
        }
    }
});

function setStatus(msg, isError = false) {
    const el = document.getElementById("status-text");
    if (!el) return;
    el.textContent = msg || "";
    el.classList.toggle("err", !!isError);
}
setStatus("Prêt");

const DebugAPI = {
    sid: null,
    async start(code, breakpoints = []) {
        const { ok, data } = await postJSON(`${API_URL}/debug/start`, { code, breakpoints }, { timeout: 15000 });
        if (!ok || data.error) throw new Error(data.error || "Erreur debug/start");
        this.sid = data.session_id;
        return data.state;
    },
    async setBreakpoints(lines = []) {
        if (!this.sid) throw new Error("Aucune session debug");
        const { ok, data } = await postJSON(`${API_URL}/debug/set_breakpoints`, { session_id: this.sid, breakpoints: lines });
        if (!ok || data.error) throw new Error(data.error || "Erreur set_breakpoints");
        return data.breakpoints;
    },
    async step() {
        if (!this.sid) throw new Error("Aucune session debug");
        const { ok, data } = await postJSON(`${API_URL}/debug/step`, { session_id: this.sid });
        if (!ok || data.error) throw new Error(data.error || "Erreur debug/step");
        return data.state;
    },
    async cont() {
        if (!this.sid) throw new Error("Aucune session debug");
        const { ok, data } = await postJSON(`${API_URL}/debug/continue`, { session_id: this.sid });
        if (!ok || data.error) throw new Error(data.error || "Erreur debug/continue");
        return data.state;
    },
    async state() {
        if (!this.sid) throw new Error("Aucune session debug");
        const url = new URL(`${API_URL}/debug/state`);
        url.searchParams.set("session_id", this.sid);
        const res = await fetch(url.toString()).then(r => r.json());
        if (res.error) throw new Error(res.error);
        return res.state;
    }
};
window.DebugAPI = DebugAPI;

console.log("MicroScript IDE ready. API:", API_URL);
