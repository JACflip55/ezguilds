interface DesignViewerProps {
  svgUrl: string;
}

export function DesignViewer({ svgUrl }: DesignViewerProps) {
  return (
    <div style={{
      flex: 1,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      background: "rgba(100,130,70,0.05)",
      overflow: "auto",
      padding: "1rem",
    }}>
      <object
        data={svgUrl}
        type="image/svg+xml"
        style={{
          maxWidth: "100%",
          maxHeight: "100%",
        }}
      >
        <p style={{ color: "var(--text-muted)" }}>Unable to load design</p>
      </object>
    </div>
  );
}
