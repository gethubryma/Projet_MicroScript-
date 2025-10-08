const API_URL = "http://127.0.0.1:5000";

const editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
    mode: "python",
    lineNumbers: true,
    indentUnit: 4,
    tabSize: 4,
});
editor.setValue(`x = 10
y = x + 5
print(y)
if y > 10:
    print(y)`);

// Sortie
const output = document.getElementById("output");
const log = document.getElementById("repl-log");
const lineInput = document.getElementById("repl-line");

//Exécution complète
document.getElementById("run-btn").addEventListener("click", async () => {
    const code = editor.getValue();
    output.textContent = "Exécution...";
    try {
        const res = await fetch(`${API_URL}/run`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code }),
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

// REPL
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

    // Affiche la ligne saisie
    log.insertAdjacentHTML("beforeend", `<div><span>&gt;&gt;&gt;</span> ${text}</div>`);
    lineInput.value = "";

    try {
        const res = await fetch(`${API_URL}/repl/exec`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ session_id: SESSION_ID, line: text }),
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
        body: JSON.stringify({ session_id: SESSION_ID }),
    });
    log.insertAdjacentHTML("beforeend", `<div> Session réinitialisée</div>`);
});
