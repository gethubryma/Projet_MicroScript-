import React from "react";

interface PropsButton {
  title : string
  onClick : React.MouseEventHandler<HTMLButtonElement> | undefined
}

const RestoreButton : React.FC<PropsButton> = ({ onClick, title }) => {

  // console.log("title : ", title)
  return (

  <button 
    onClick={onClick} 
    title='Ouvrir'
    className="w-5 h-5 rounded-full bg-blue-950 text-white flex items-center justify-center cursor-pointer transition-transform hover:scale-110"
  > 
  {title}
  </button>
  )
};

export default RestoreButton