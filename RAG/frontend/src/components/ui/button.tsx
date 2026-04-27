import React from "react";

type BtnProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  children?: React.ReactNode;
};

export default function Button({ children, ...props }: BtnProps) {
  return (
    <button className="btn" {...props}>
      {children}
    </button>
  );
}
