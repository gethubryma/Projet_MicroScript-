import React from "react";
import { examples } from "../examples";
import { Link } from "react-router-dom";

type ExamplesDropdownProps = {
  setCode: (code: string) => void;
};

const ExamplesDropdown: React.FC<ExamplesDropdownProps> = ({ setCode }) => {
  const handleExampleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedExampleName = event.target.value;
    const example = examples.find((ex) => ex.name === selectedExampleName);
    if (example) {
      setCode(example.code);
    }
  };

  return (
    <div className="flex gap-2">
      <select
        onChange={handleExampleChange}
        className="bg-gray-700 text-white p-2 rounded-lg text-sm border-2 border-transparent focus:border-sky-500 focus:outline-none cursor-pointer"
        defaultValue=""
      >
        <option value="" disabled>
          Charger un exemple...
        </option>
        {examples.map((example) => (
          <option key={example.name} value={example.name}>
            {example.name}
          </option>
        ))}
      </select>
      <button className="text-white bg-gradient-to-tr from-[#090142] to-[#080132] hover:bg-indigo-50 p-2 rounded-md">
        <Link to={"http://195.15.242.96:2801/documentation"}>
          Documentation
        </Link>
      </button>
    </div>
  );
};

export default ExamplesDropdown;
