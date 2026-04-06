import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { NavBar } from "../components/NavBar";
import { FileDropZone } from "../components/FileDropZone";
import { createProject, uploadFile } from "../api";

interface UploadedFile {
  name: string;
  type: string;
  size: number;
}

function guessFileType(file: File): string {
  const name = file.name.toLowerCase();
  if (name.includes("site") || name.includes("map") || name.includes("aerial")) return "site_map";
  if (name.includes("soil")) return "soil_test";
  if (file.type.startsWith("image/")) return "photo";
  return "other";
}

export function UploadPage() {
  const { getToken } = useAuth();
  const navigate = useNavigate();
  const [projectId, setProjectId] = useState<string | null>(null);
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [uploading, setUploading] = useState(false);

  const hasSiteMap = files.some((f) => f.type === "site_map");

  const handleFiles = async (newFiles: File[]) => {
    setUploading(true);
    const token = await getToken();

    let pid = projectId;
    if (!pid) {
      const project = await createProject(token);
      pid = project.id;
      setProjectId(pid);
    }

    for (const file of newFiles) {
      const fileType = guessFileType(file);
      await uploadFile(token, pid!, file, fileType);
      setFiles((prev) => [...prev, { name: file.name, type: fileType, size: file.size }]);
    }
    setUploading(false);
  };

  const handleContinue = () => {
    if (projectId) navigate(`/project/${projectId}/questions`);
  };

  return (
    <div>
      <NavBar currentStep={0} />
      <div style={{ maxWidth: "640px", margin: "2rem auto", padding: "0 1.5rem" }}>
        <h2 style={{ marginBottom: "0.5rem" }}>Start Your Design</h2>
        <p style={{ color: "var(--text-muted)", marginBottom: "1.5rem" }}>
          Upload your site info to get started
        </p>

        <FileDropZone onFiles={handleFiles} />

        {files.length > 0 && (
          <div style={{ marginTop: "1rem" }}>
            {files.map((f, i) => (
              <div key={i} style={{
                background: "var(--bg-elevated)",
                borderRadius: "6px",
                padding: "0.75rem",
                marginBottom: "0.5rem",
                fontSize: "0.85rem",
                display: "flex",
                justifyContent: "space-between",
              }}>
                <span>
                  <span style={{ color: "var(--accent-green-light)" }}>✓ </span>
                  {f.name}
                </span>
                <span style={{ color: "var(--text-faint)" }}>
                  {(f.size / 1024).toFixed(0)} KB
                </span>
              </div>
            ))}
          </div>
        )}

        {uploading && (
          <p style={{ color: "var(--text-muted)", marginTop: "1rem", fontSize: "0.85rem" }}>
            Uploading...
          </p>
        )}

        <button
          onClick={handleContinue}
          disabled={!hasSiteMap}
          style={{
            width: "100%",
            marginTop: "1.5rem",
            opacity: hasSiteMap ? 1 : 0.4,
            cursor: hasSiteMap ? "pointer" : "not-allowed",
          }}
        >
          Continue to Questions →
        </button>

        {!hasSiteMap && files.length > 0 && (
          <p style={{ color: "var(--text-faint)", fontSize: "0.8rem", marginTop: "0.5rem", textAlign: "center" }}>
            A site map is required to continue. Upload a file with "site" or "map" in the name, or rename your file.
          </p>
        )}
      </div>
    </div>
  );
}
