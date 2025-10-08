// frontend/src/Editor.jsx
import { useEffect, useImperativeHandle, useRef, useState, forwardRef } from "react";
import BreakpointGutter from "./breakpointGutter";

const DEFAULT_SAMPLE = `x = 10
y = x + 5
print(y)
if y > 10:
    print(y)`;

const Editor = forwardRef(function Editor(
    {
        initialValue = DEFAULT_SAMPLE,
        mode = "python",
        readOnly = false,
        height = 360,
        breakpoints = [],
        onChange,
        onRun,
        onRunTimed,
        onFormat,
        onToggleBreakpoint
    },
    ref
) {
    const [value, setValue] = useState(initialValue);
    const [bps, setBps] = useState(Array.isArray(breakpoints) ? breakpoints : []);
    const cmRef = useRef(null);

    useEffect(() => {
        setValue(initialValue);
    }, [initialValue]);

    useEffect(() => {
        setBps(Array.isArray(breakpoints) ? breakpoints : []);
    }, [breakpoints]);

    function handleChange(v) {
        setValue(v);
        onChange?.(v);
    }

    function handleFormat() {
        const formatted = value.split("\n").map(s => s.replace(/\t/g, "    ")).join("\n");
        setValue(formatted);
        if (cmRef.current && cmRef.current.getValue() !== formatted) {
            cmRef.current.setValue(formatted);
        }
        onFormat?.(formatted);
    }

    function handleToggleBreakpoint(lineNumber) {
        let next = new Set(bps);
        if (next.has(lineNumber)) next.delete(lineNumber);
        else next.add(lineNumber);
        const out = Array.from(next).sort((a, b) => a - b);
        setBps(out);
        onToggleBreakpoint?.(lineNumber, out);
    }

    function focus() {
        try { cmRef.current?.focus(); } catch { }
    }

    useEffect(() => {
        const isMac = navigator.platform.toUpperCase().includes("MAC");
        function onKey(e) {
            const mod = isMac ? e.metaKey : e.ctrlKey;
            if (mod && e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                onRun?.(value);
            } else if (!mod && e.key === "Enter" && e.shiftKey) {
                const evt = new CustomEvent("editor-shift-enter", { detail: { code: value } });
                window.dispatchEvent(evt);
            } else if (mod && e.key.toLowerCase() === "b") {
                e.preventDefault();
                try {
                    const doc = cmRef.current?.getDoc();
                    const cur = doc?.getCursor();
                    if (!cur) return;
                    handleToggleBreakpoint(cur.line + 1);
                } catch { }
            }
        }
        window.addEventListener("keydown", onKey);
        return () => window.removeEventListener("keydown", onKey);
    }, [value, onRun]);

    useImperativeHandle(ref, () => ({
        getValue: () => value,
        setValue: (v) => {
            setValue(String(v ?? ""));
            if (cmRef.current && cmRef.current.getValue() !== v) cmRef.current.setValue(String(v ?? ""));
        },
        focus,
        format: handleFormat,
        getBreakpoints: () => [...bps],
        setBreakpoints: (arr) => setBps(Array.isArray(arr) ? arr : []),
        getEditor: () => cmRef.current
    }));

    return (
        <div className="panel" style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            <div className="toolbar">
                <span className="badge">Éditeur</span>
                <div className="spacer" />
                <button type="button" className="btn" onClick={() => onRun?.(value)}>Exécuter</button>
                <button type="button" className="btn btn-secondary" onClick={() => onRunTimed?.(value)}>⏱ Exécuter</button>
                <button type="button" className="btn btn-ghost" onClick={handleFormat} title="Remplacer tabulations par 4 espaces">Format</button>
            </div>

            <div style={{ height }}>
                <BreakpointGutter
                    value={value}
                    mode={mode}
                    readOnly={readOnly}
                    tabSize={4}
                    indentUnit={4}
                    lineNumbers
                    breakpoints={bps}
                    onChange={handleChange}
                    onToggleBreakpoint={handleToggleBreakpoint}
                    onEditorReady={(cm) => {
                        cmRef.current = cm;
                        try {
                            cm.setSize("100%", height);
                            cm.setOption("styleActiveLine", true);
                            cm.setOption("matchBrackets", true);
                        } catch { }
                    }}
                />
            </div>

            <div className="statusbar">
                <span className="dot" aria-hidden="true"></span>
                <span className="text-dim">Ctrl/⌘+Entrée: Exécuter — Shift+Entrée: REPL — Ctrl/⌘+B: Toggle Breakpoint</span>
            </div>
        </div>
    );
});

export default Editor;
