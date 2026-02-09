import React from "react";
import WindowHeader from "./WindowHeader";

interface PropsOutPut {
  output: string;
  isMinimized: boolean;
  isMaximized: boolean;
  isVisible: boolean;
  onToggleMinimize: () => void;
  onToggleMaximize: () => void;
  onClose: () => void;
}

const Terminal: React.FC<PropsOutPut> = ({
  output,
  isVisible,
  isMinimized,
  isMaximized,
  onToggleMinimize,
  onToggleMaximize,
  onClose,
}) => {
  const status = output.includes("Erreur");

  // Combinaison des classes Tailwind pour gérer les états d'affichage
  const terminalClasses = `
    flex-1 bg-[#1e1e1e] rounded-r-lg shadow-2xl overflow-hidden flex flex-col
    transition-all duration-300
    ${isMaximized ? "fixed inset-0 z-50 rounded-lg" : ""}
    ${isMinimized ? "flex-grow-0 !flex-shrink-0" : ""}
    ${!isVisible ? "hidden" : ""}
  `;
  return (
    <div className={terminalClasses}>
      <WindowHeader
        onClose={onClose}
        onMinimize={onToggleMinimize}
        onMaximize={onToggleMaximize}
      >
        <span className="ml-5 text-xs text-gray-400 font-bold tracking-widest">
          TERMINAL
        </span>
      </WindowHeader>
      {!isMinimized && (
        <pre
          className={`p-4 font-mono text-sm flex-grow overflow-y-auto whitespace-pre-wrap break-words ${
            !status ? "text-green-400" : "text-red-500"
          }`}
        >
          {output}
        </pre>
      )}
    </div>
  );
};

export default Terminal;
