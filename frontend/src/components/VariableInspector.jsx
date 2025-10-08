// frontend/src/VariableInspector.jsx
import { useMemo } from "react";

function Entry({ k, v }) {
    const type = typeof v;
    let display = v;

    if (v === null) display = "null";
    else if (v === undefined) display = "undefined";
    else if (Array.isArray(v)) display = `[${v.map(x => stringify(x)).join(", ")}]`;
    else if (type === "object") display = `{ ${Object.keys(v).slice(0, 6).map(x => `${x}: ${stringify(v[x])}`).join(", ")}${Object.keys(v).length > 6 ? ", …" : ""} }`;
    else display = stringify(v);

    return (
        <div className="card">
            <h3 title={k}>{k}</h3>
            <div className="kv">
                <span className="text-dim">type</span>
                <span>{prettyType(v)}</span>
            </div>
            <div className="kv">
                <span className="text-dim">valeur</span>
                <span title={typeof display === "string" ? display : String(display)}>{String(display)}</span>
            </div>
        </div>
    );
}

function stringify(x) {
    if (typeof x === "string") return `"${x}"`;
    if (typeof x === "number" && !Number.isFinite(x)) return String(x);
    if (typeof x === "function") return "<fn>";
    if (x === null) return "null";
    if (x === undefined) return "undefined";
    if (Array.isArray(x)) return `[${x.map(stringify).join(", ")}]`;
    if (typeof x === "object") {
        try {
            return JSON.stringify(x);
        } catch {
            return "{…}";
        }
    }
    return String(x);
}

function prettyType(v) {
    if (Array.isArray(v)) return "list";
    if (v === null) return "null";
    if (v === undefined) return "undefined";
    if (typeof v === "object") return "dict";
    return typeof v;
}

export default function VariableInspector({
    variables = {},
    title = "Variables",
    sortable = true,
    sortDir = "asc",
    filter = "",
    onRefresh,
}) {
    const entries = useMemo(() => {
        let pairs = Object.entries(variables || {});
        if (filter && filter.trim()) {
            const f = filter.trim().toLowerCase();
            pairs = pairs.filter(([k, v]) => k.toLowerCase().includes(f) || stringify(v).toLowerCase().includes(f));
        }
        if (sortable) {
            pairs.sort(([a], [b]) => sortDir === "desc" ? b.localeCompare(a) : a.localeCompare(b));
        }
        return pairs;
    }, [variables, sortable, sortDir, filter]);

    async function handleCopyAll() {
        const text = entries.map(([k, v]) => `${k} = ${stringify(v)}`).join("\n");
        try {
            await navigator.clipboard.writeText(text);
        } catch { }
    }

    return (
        <section className="panel" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <div className="toolbar">
                <span className="badge">{title}</span>
                <div className="spacer" />
                <button className="btn btn-ghost" type="button" onClick={handleCopyAll}>Copier</button>
                {onRefresh ? (
                    <button className="btn btn-secondary" type="button" onClick={onRefresh}>Rafraîchir</button>
                ) : null}
            </div>

            <div className="inspector">
                {entries.length === 0 ? (
                    <div className="text-dim">Aucune variable.</div>
                ) : (
                    entries.map(([k, v]) => <Entry key={k} k={k} v={v} />)
                )}
            </div>
        </section>
    );
}
