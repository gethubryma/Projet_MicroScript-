import { useEffect, useRef } from "react";

export default function BreakpointGutter({
    value = "",
    mode = "python",
    lineNumbers = true,
    tabSize = 4,
    indentUnit = 4,
    readOnly = false,
    breakpoints = [],
    onChange,
    onToggleBreakpoint,
    onEditorReady,
}) {
    const hostRef = useRef(null);
    const cmRef = useRef(null);
    const bpSetRef = useRef(new Set());

    useEffect(() => {
        if (!hostRef.current || cmRef.current) return;
        const cm = window.CodeMirror(hostRef.current, {
            value,
            mode,
            lineNumbers,
            tabSize,
            indentUnit,
            readOnly,
            styleActiveLine: true,
            matchBrackets: true,
            gutters: ["CodeMirror-linenumbers", "breakpoints"],
            theme: undefined,
        });
        cm.on("change", (inst, chg) => {
            if (onChange) onChange(inst.getValue(), chg);
        });
        cm.on("gutterClick", (_inst, line, _gutter, _event) => {
            const ln = line + 1;
            if (onToggleBreakpoint) onToggleBreakpoint(ln);
        });
        cmRef.current = cm;
        if (onEditorReady) onEditorReady(cm);
    }, [hostRef, onChange, onToggleBreakpoint, onEditorReady, value, mode, lineNumbers, tabSize, indentUnit, readOnly]);

    useEffect(() => {
        const cm = cmRef.current;
        if (!cm) return;
        const next = new Set(breakpoints.map((n) => Number(n) || 0).filter((n) => n > 0));
        const prev = bpSetRef.current;

        prev.forEach((ln) => {
            if (!next.has(ln)) {
                cm.setGutterMarker(ln - 1, "breakpoints", null);
            }
        });

        next.forEach((ln) => {
            if (!prev.has(ln)) {
                const marker = document.createElement("div");
                marker.className = "breakpoint-marker";
                cm.setGutterMarker(ln - 1, "breakpoints", marker);
            }
        });

        bpSetRef.current = next;
    }, [breakpoints]);

    useEffect(() => {
        const cm = cmRef.current;
        if (!cm) return;
        if (cm.getValue() !== value) cm.setValue(value);
    }, [value]);

    useEffect(() => {
        const cm = cmRef.current;
        if (!cm) return;
        cm.setOption("readOnly", readOnly);
    }, [readOnly]);

    useEffect(() => {
        const cm = cmRef.current;
        if (!cm) return;
        cm.setOption("mode", mode);
    }, [mode]);

    useEffect(() => {
        const cm = cmRef.current;
        if (!cm) return;
        cm.setOption("tabSize", tabSize);
        cm.setOption("indentUnit", indentUnit);
    }, [tabSize, indentUnit]);

    useEffect(() => {
        const cm = cmRef.current;
        return () => {
            if (!cm) return;
            cm.toTextArea?.();
            cmRef.current = null;
        };
    }, []);

    return <div ref={hostRef} style={{ height: "100%" }} />;
}
