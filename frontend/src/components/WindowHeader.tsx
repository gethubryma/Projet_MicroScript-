import type { ReactNode } from "react";

interface PropsWindow {
  children: ReactNode;
  onClose: () => void;
  onMinimize: () => void;
  onMaximize: () => void;
}

const WindowHeader: React.FC<PropsWindow> = ({
  children,
  onClose,
  onMinimize,
  onMaximize,
}) => (
  <div className="flex flex-col p-3 bg-[#1e1e1e] border-b border-white/10">
    <div className="flex gap-2 mb-2.5">
      <span
        onClick={onClose}
        className="w-3 h-3 rounded-full bg-[#ff5f56]"
      ></span>
      <span
        onClick={onMinimize}
        className="w-3 h-3 rounded-full bg-[#ffbd2e]"
      ></span>
      <span
        onClick={onMaximize}
        className="w-3 h-3 rounded-full bg-[#27c93f]"
      ></span>
    </div>
    {children}
  </div>
);

export default WindowHeader;
