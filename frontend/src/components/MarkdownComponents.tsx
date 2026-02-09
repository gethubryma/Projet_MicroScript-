/* eslint-disable @typescript-eslint/no-explicit-any */
// src/components/MarkdownComponents.tsx

import React, { useState, type ReactNode } from "react";
import { Copy, Check } from "lucide-react";

// ... (Les composants StyledH2 et StyledH3 ne changent pas) ...
export const StyledH2 = ({ children }: { children?: ReactNode }) => (
  <h2 className="text-3xl font-bold text-sky-400 mt-12 mb-6 pb-3 border-b-2 border-gray-700 flex items-center gap-3">
    {children}
  </h2>
);
export const StyledH3 = ({ children }: { children?: ReactNode }) => (
  <h3 className="text-2xl font-semibold text-green-400 mt-8 mb-4">
    {children}
  </h3>
);

// --- Composant pour les blocs de code ---
export const CodeBlock = ({ children }: { children?: any }) => {
  const [hasCopied, setHasCopied] = useState(false);

  const codeToCopy = React.Children.toArray(children)
    .flat()
    .map((child) => {
      // On vérifie si c'est un élément React valide
      if (React.isValidElement(child)) {
        // ✅ CORRECTION ICI : On affirme le type de child.props
        const props = child.props as { children?: ReactNode };
        return props.children;
      }
      return child;
    })
    .join("");

  const copyToClipboard = () => {
    if (codeToCopy) {
      navigator.clipboard.writeText(codeToCopy);
      setHasCopied(true);
      setTimeout(() => setHasCopied(false), 2000);
    }
  };

  return (
    <div className="bg-[#161b22] border border-gray-700 rounded-lg my-6 relative">
      <div className="absolute top-2 right-2">
        <button
          onClick={copyToClipboard}
          className="p-2 bg-gray-700 rounded-md text-gray-400 hover:bg-gray-600 hover:text-white transition-all"
          title="Copier le code"
        >
          {hasCopied ? (
            <Check size={16} className="text-green-400" />
          ) : (
            <Copy size={16} />
          )}
        </button>
      </div>
      <pre className="p-4 pt-10 font-mono text-sm text-gray-300 overflow-x-auto">
        {children}
      </pre>
    </div>
  );
};
