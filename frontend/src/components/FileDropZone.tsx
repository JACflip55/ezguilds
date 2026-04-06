import { useCallback, useState, DragEvent } from "react";

interface FileDropZoneProps {
  onFiles: (files: File[]) => void;
  accept?: string;
}

export function FileDropZone({ onFiles, accept }: FileDropZoneProps) {
  const [dragging, setDragging] = useState(false);

  const handleDrop = useCallback(
    (e: DragEvent) => {
      e.preventDefault();
      setDragging(false);
      const files = Array.from(e.dataTransfer.files);
      if (files.length > 0) onFiles(files);
    },
    [onFiles]
  );

  const handleClick = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.multiple = true;
    if (accept) input.accept = accept;
    input.onchange = () => {
      if (input.files) onFiles(Array.from(input.files));
    };
    input.click();
  };

  return (
    <div
      onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={handleClick}
      style={{
        border: `2px dashed ${dragging ? "var(--accent-green-light)" : "var(--border)"}`,
        borderRadius: "8px",
        padding: "2rem",
        textAlign: "center",
        cursor: "pointer",
        transition: "border-color 0.2s",
      }}
    >
      <p style={{ fontSize: "0.9rem", color: "var(--text-secondary)" }}>
        Drop files here or click to browse
      </p>
      <p style={{ fontSize: "0.75rem", color: "var(--text-faint)", marginTop: "0.5rem" }}>
        Site map (required) + goals doc (recommended) + optional extras
      </p>
    </div>
  );
}
