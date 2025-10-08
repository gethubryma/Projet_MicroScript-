import { useEffect, useImperativeHandle, useMemo, useRef, useState, forwardRef } from "react";

const Console = forwardRef(function Console(
    {
        logs = [],
        autoScroll = true,
        height = 220,
        placeholder = "Tape une ligne puis Entrée…",
        showControls = true,
        readOnlyInput = false,
        initialInput = "",
        onSubmit,
        onClear,
        onCopy,
        className = "",
    },
    ref
) {
    const [input, setInput] = useState(initialInput);
    const listRef = useRef(null);
    const inputRef = useRef(null);
    const localLogsRef = useRef([...logs]);

    const allLogs = useMemo(() => {
        return localLogsRef.current;
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [logs]);

    useEffect(() => {
        localLogsRef.current = [...logs];
        if (autoScroll) {
            requestAnimationFrame(() => {
                if (listRef.current) listRef.current.scrollTop = listRef.current.scrollHeight;
            });
        }
    }, [logs, autoScroll]);

    useImperativeHandle(ref, () => ({
        append(text, type = "out") {
            localLogsRef.current = [...localLogsRef.current, { text: String(text ?? ""), type }];
            if (listRef.current) {
                const div = document.createElement("div");
                div.className = `line ${type === "err" ? "err" : type === "ok" ? "ok" : ""}`;
                div.textContent = String(text ?? "");
                listRef.current.appendChild(div);
                if (autoScroll) listRef.current.scrollTop = listRef.current.scrollHeight;
            }
        },
        clear() {
            localLogsRef.current = [];
            if (listRef.current) listRef.current.innerHTML = "";
        },
        focusInput() {
            inputRef.current?.focus();
        },
    }));

    function handleKeyDown(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            const text = input.trimEnd();
            if (!text) return;
            if (onSubmit) onSubmit(text);
            setInput("");
        }
    }

    function handleClear() {
        if (onClear) onClear();
        localLogsRef.current = [];
        if (listRef.current) listRef.current.innerHTML = "";
    }

    async function handleCopy() {
        const txt = (localLogsRef.current || []).map(l => l.text).join("\n");
        try {
            await navigator.clipboard.writeText(txt);
            if (onCopy) onCopy(true);
        } catch {
            if (onCopy) onCopy(false);
        }
    }

    return (
        <div className={`console ${className}`} style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {showControls && (
                <div className="toolbar">
                    <span className="badge">Console</span>
                    <div className="spacer" />
                    <button className="btn btn-ghost" type="button" onClick={handleCopy}>Copier</button>
                    <button className="btn btn-secondary" type="button" onClick={handleClear}>Effacer</button>
                </div>
            )}

            <div
                ref={listRef}
                className="terminal"
                style={{ height }}
                aria-live="polite"
            >
                {allLogs.length === 0 ? (
                    <div className="text-dim">Aucune sortie.</div>
                ) : (
                    allLogs.map((l, i) => (
                        <div
                            key={i}
                            className={`line ${l.type === "err" ? "err" : l.type === "ok" ? "ok" : ""}`}
                        >
                            {l.type === "cmd" ? <span className="prompt">&gt;&gt;&gt;</span> : null}
                            {String(l.text ?? "")}
                        </div>
                    ))
                )}
            </div>

            <div className="repl-input">
                <span>&gt;&gt;&gt;</span>
                <input
                    ref={inputRef}
                    id="console-input"
                    type="text"
                    placeholder={placeholder}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={readOnlyInput}
                />
                <button className="btn" type="button" onClick={() => onSubmit?.(input) || setInput("")}>Entrer</button>
            </div>
        </div>
    );
});

export default Console;
