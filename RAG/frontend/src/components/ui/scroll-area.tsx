import React from "react";

export default function ScrollArea({
  children,
}: {
  children?: React.ReactNode;
}) {
  return <div className="scroll-area">{children}</div>;
}
