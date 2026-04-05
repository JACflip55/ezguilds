import { useAuth } from "../hooks/useAuth";

export function LoginPage() {
  const { signIn } = useAuth();

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      minHeight: "100vh",
      gap: "1.5rem",
    }}>
      <h1 style={{ fontSize: "2rem" }}>EZGuilds</h1>
      <p style={{ color: "var(--text-muted)" }}>
        AI-powered permaculture design
      </p>
      <button onClick={signIn}>Sign in with Google</button>
    </div>
  );
}
