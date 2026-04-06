import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthContext, useAuthProvider, useAuth } from "./hooks/useAuth";
import { LoginPage } from "./pages/LoginPage";
import { UploadPage } from "./pages/UploadPage";

function AuthGate({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "100vh",
        color: "var(--text-muted)",
      }}>
        Loading...
      </div>
    );
  }

  if (!user) return <LoginPage />;
  return <>{children}</>;
}

export function App() {
  const authState = useAuthProvider();

  return (
    <AuthContext.Provider value={authState}>
      <BrowserRouter>
        <AuthGate>
          <Routes>
            <Route path="/" element={<UploadPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </AuthGate>
      </BrowserRouter>
    </AuthContext.Provider>
  );
}
