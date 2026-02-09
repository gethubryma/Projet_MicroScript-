import { RefreshCcw } from "lucide-react";
import React from "react";
import RestoreButton from "../ui/RestoreButton";
import ExamplesDropdown from "./ExamplesDropdown";

interface PropsOnRun {
  load: boolean;
  onRun: React.MouseEventHandler<HTMLButtonElement>;
  isEditorVisible: boolean;
  isTerminalVisible: boolean;
  setIsEditorVisible: React.Dispatch<React.SetStateAction<boolean>>;
  setIsTerminalVisible: React.Dispatch<React.SetStateAction<boolean>>;
  setCode: (code: string) => void;
}

const Header: React.FC<PropsOnRun> = ({
  onRun,
  load,
  isEditorVisible,
  setIsEditorVisible,
  isTerminalVisible,
  setIsTerminalVisible,
  setCode,
}) => {
  // console.log("test : ", isEditorVisible, isTerminalVisible)

  return (
    <header className="flex justify-between items-center mb-5">
      <div>
        <h1
          className="text-white text-sm md:text-2xl font-semibold tracking-wide"
          style={{ textShadow: "0 0 10px rgba(255,255,255,0.2)" }}
        >
          LAXA MONOSCRIPT
        </h1>
        {/* NOUVEAU : Zone pour les boutons de restauration */}
        <div className="flex items-center gap-2">
          {!isEditorVisible && (
            <RestoreButton onClick={() => setIsEditorVisible(true)} title=">" />
          )}
          {!isTerminalVisible && (
            <RestoreButton
              onClick={() => setIsTerminalVisible(true)}
              title=">"
            />
          )}
        </div>
      </div>
      <ExamplesDropdown setCode={setCode} /> {/* ✅ Ajouter le composant ici */}
      <button
        onClick={onRun}
        className="flex items-center cursor-pointer hover:bg-teal-600 text-sm md:text-base gap-2 px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
      >
        {load ? (
          <RefreshCcw size={20} className="animate-spin" />
        ) : (
          <RefreshCcw size={20} />
        )}
        <span>{load ? "Exécution..." : "Exécuter"}</span>
      </button>
    </header>
  );
};

export default Header;
