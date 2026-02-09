import React, { useState } from "react";
import { Link } from "react-router-dom";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import { documentationSections } from "../../documentation";
import {
  CodeBlock,
  StyledH2,
  StyledH3,
} from "../../components/MarkdownComponents";

// --- Sous-composant pour le Header ---
const Header = () => (
  <header className="fixed top-0 left-0 right-0 h-16 bg-[#161b22] border-b border-gray-800 flex items-center justify-between px-6 z-10">
    <Link to="/" className="flex items-center gap-3">
      <div className="bg-[#21262d] p-2 rounded-md text-xl">🇫🇷</div>
      <div>
        <h1 className="text-xl font-bold text-white">LAXA MONOSCRIPT IDE</h1>
        <p className="text-xs text-gray-400">
          Mon Langage de Programmation Français
        </p>
      </div>
    </Link>
    <div className="flex items-center gap-4">
      <Link
        to="/"
        className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-gray-700 rounded-md hover:bg-gray-600"
      >
        💻 IDE
      </Link>
      <Link
        to="/documentation"
        className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700"
      >
        📚 Documentation
      </Link>
    </div>
  </header>
);

// --- Sous-composant pour la Sidebar ---
type SidebarProps = {
  activeSectionId: string;
  setActiveSectionId: (id: string) => void;
};

const Sidebar: React.FC<SidebarProps> = ({
  activeSectionId,
  setActiveSectionId,
}) => (
  <aside className="fixed top-16 left-0 w-64 h-[calc(100vh-64px)] bg-[#161b22] border-r border-gray-800 p-6 overflow-y-auto">
    <h2 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-4">
      Navigation
    </h2>
    <nav className="flex flex-col gap-2">
      {documentationSections.map((section) => (
        <button
          key={section.id}
          onClick={() => setActiveSectionId(section.id)}
          className={`text-left text-sm px-4 py-2 rounded-md transition-colors duration-200 ${
            activeSectionId === section.id
              ? "bg-sky-500/10 text-sky-400 font-semibold"
              : "text-gray-400 hover:bg-gray-700/50 hover:text-white"
          }`}
        >
          {section.title}
        </button>
      ))}
    </nav>
  </aside>
);

// --- Composant Principal de la Page ---
function DocsPage() {
  // ✅ L'état pour suivre la section active
  const [activeSectionId, setActiveSectionId] = useState(
    documentationSections[0].id
  );

  // ✅ On trouve le contenu de la section à afficher
  const currentSection = documentationSections.find(
    (section) => section.id === activeSectionId
  );

  return (
    <div className="min-h-screen bg-[#0d1117] text-gray-300 font-sans">
      <Header />

      <div className="flex pt-16">
        <Sidebar
          activeSectionId={activeSectionId}
          setActiveSectionId={setActiveSectionId}
        />

        <main className="ml-64 p-8 w-full">
          <div className="max-w-4xl">
            <article className="max-w-none">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                // ✅ On indique à ReactMarkdown quels composants utiliser pour chaque balise
                components={{
                  h2: StyledH2,
                  h3: StyledH3,
                  pre: CodeBlock,
                }}
              >
                {currentSection
                  ? currentSection.content
                  : "Section non trouvée."}
              </ReactMarkdown>
            </article>
          </div>
        </main>
      </div>
    </div>
  );
}

export default DocsPage;
