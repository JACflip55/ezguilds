import { useAuth } from "../hooks/useAuth";

const STEPS = ["Upload", "Questions", "Design", "Review"];

interface NavBarProps {
  currentStep: number; // 0-indexed
}

export function NavBar({ currentStep }: NavBarProps) {
  const { logOut } = useAuth();

  return (
    <nav style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      padding: "0.75rem 1.5rem",
      background: "var(--bg-surface)",
      borderBottom: "1px solid var(--border-light)",
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
        <h1 style={{ fontSize: "1.1rem", margin: 0 }}>EZGuilds</h1>
        <div style={{ display: "flex", gap: "0.5rem", fontSize: "0.85rem" }}>
          {STEPS.map((step, i) => (
            <span key={step} style={{
              color: i === currentStep
                ? "var(--accent-green-heading)"
                : i < currentStep
                  ? "var(--accent-green-light)"
                  : "var(--text-faint)",
              fontWeight: i === currentStep ? 600 : 400,
            }}>
              {i > 0 && <span style={{ margin: "0 0.25rem", color: "var(--text-faint)" }}> → </span>}
              {step}
            </span>
          ))}
        </div>
      </div>
      <button
        onClick={logOut}
        style={{
          background: "transparent",
          border: "1px solid var(--border)",
          fontSize: "0.8rem",
          padding: "0.3rem 0.75rem",
          color: "var(--text-muted)",
        }}
      >
        Sign out
      </button>
    </nav>
  );
}
