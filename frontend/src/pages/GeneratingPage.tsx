import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { usePolling } from "../hooks/usePolling";
import { NavBar } from "../components/NavBar";
import { getStatus } from "../api";

export function GeneratingPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const { getToken } = useAuth();
  const navigate = useNavigate();

  const { data } = usePolling(
    async () => {
      const token = await getToken();
      return getStatus(token, projectId!);
    },
    3000,
    true
  );

  useEffect(() => {
    if (data?.design_status === "complete") {
      navigate(`/project/${projectId}/review`);
    }
  }, [data]);

  const isFailed = data?.design_status === "failed";

  return (
    <div>
      <NavBar currentStep={2} />
      <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "70vh",
        gap: "1rem",
      }}>
        {isFailed ? (
          <>
            <div style={{ fontSize: "2rem" }}>⚠️</div>
            <h3>Generation Failed</h3>
            <p style={{ color: "var(--text-muted)" }}>
              Something went wrong. Please try again.
            </p>
            <button onClick={() => navigate(`/project/${projectId}/questions`)}>
              ← Back to Questions
            </button>
          </>
        ) : (
          <>
            <div style={{ fontSize: "2rem" }}>🌱</div>
            <h3>Generating Your Design</h3>
            <p style={{ color: "var(--text-muted)" }}>
              Analyzing your site map, goals, and answers...
            </p>
            <div style={{
              background: "rgba(100,130,70,0.15)",
              borderRadius: "4px",
              height: "6px",
              overflow: "hidden",
              width: "300px",
            }}>
              <div style={{
                background: "var(--accent-green-light)",
                height: "100%",
                width: "65%",
                borderRadius: "4px",
                animation: "pulse 2s ease-in-out infinite",
              }} />
            </div>
            <p style={{ fontSize: "0.75rem", color: "var(--text-faint)" }}>
              Classifying scale... Mapping zones... Selecting guilds...
            </p>
          </>
        )}
      </div>
    </div>
  );
}
