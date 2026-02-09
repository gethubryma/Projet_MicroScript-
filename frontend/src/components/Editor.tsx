import React from 'react';
import CodeMirror from '@uiw/react-codemirror';
// import { javascript } from '@codemirror/lang-javascript';
import { dracula } from '@uiw/codemirror-theme-dracula';
import WindowHeader from './WindowHeader';
import { monoscriptLanguage, monoscriptTheme } from '../monoscript-lang';
// ✅ Importer les deux nouvelles extensions séparément





interface PropsEditor {
  isMinimized:boolean;
  isMaximized:boolean;
  isVisible:boolean;
  code : string;
  setCode : React.Dispatch<React.SetStateAction<string>>
  onToggleMinimize : () => void
  onToggleMaximize : () => void
  onClose : () => void
}


const Editor : React.FC<PropsEditor> = ({ code, setCode, isVisible, isMinimized, isMaximized, onToggleMinimize, onToggleMaximize, onClose }) =>{
  // On combine les classes Tailwind conditionnellement
  const editorClasses = `
    flex-[1.5] bg-[#282a36] rounded-l-lg shadow-2xl overflow-hidden flex flex-col
    transition-all duration-300
    ${isMaximized ? 'fixed inset-0 z-50 rounded-lg' : ''}
    ${isMinimized ? 'flex-grow-0 !flex-shrink-0' : ''}
    ${!isVisible ? 'hidden' : ''}
  `;
  
  return (
    <div className={editorClasses}>
      <WindowHeader 
      onMinimize={onToggleMinimize}
        onMaximize={onToggleMaximize}
        onClose={onClose}>
      {!isMinimized && (
        <CodeMirror
          value={code}
          height={isMaximized ? "100vh" : "500px"}
          theme={dracula}

          // ✅ Utiliser les deux extensions dans le tableau
          extensions={[monoscriptLanguage, monoscriptTheme]}
          // extensions={[javascript({ jsx: true })]}
          onChange={(value) => setCode(value)}
          className="flex-grow"
          style={{ fontFamily: "'Fira Code', monospace" }}
        />
      )}

      </WindowHeader >
      
    </div>
  );
}

export default Editor;