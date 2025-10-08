// frontend/src/Toolbar.jsx
import React from "react";

export default function Toolbar({
    onRun,
    onRunTimed,
    onFormat,
    onDebugStart,
    onDebugStep,
    onDebugContinue,
    onResetRepl,
    statusText = "Prêt",
    statusError = false,
    breakpoints = [],
    right = null,
}) {
    return (
        <div className="toolbar">
            <span className="badge">Outils</span>
            <button type="button" className="btn" onClick={onRun}>Exécuter</button>
            <button type="button" className="btn btn-secondary" onClick={onRunTimed}>⏱ Exécuter</button>
            <button type="button" className="btn btn-ghost" onClick={onFormat} title="Formater">Format</button>
            <div className="spacer" />
            <span className="badge">Breakpoints</span>
            <span id="dbg-bp" className="text-dim">{Array.isArray(breakpoints) ? breakpoints.length : 0}</span>
            <button type="button" className="btn" onClick={onDebugStart}>Debug</button>
            <button type="button" className="btn btn-secondary" onClick={onDebugStep}>Step</button>
            <button type="button" className="btn btn-secondary" onClick={onDebugContinue}>Continue</button>
            <button type="button" className="btn btn-ghost" onClick={onResetRepl} title="Réinitialiser REPL">↺ REPL</button>
            {right}
            <div className="statusbar">
                <span className={`dot${statusError ? " err" : ""}`} aria-hidden="true"></span>
                <span id="status-text">{statusText}</span>
            </div>
        </div>
    );
}
