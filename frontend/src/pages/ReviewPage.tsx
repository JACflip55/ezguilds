import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { NavBar } from "../components/NavBar";
import { DesignViewer } from "../components/DesignViewer";
import { ChatSidebar } from "../components/ChatSidebar";
import { getDesign, sendChatMessage, getStatus } from "../api";
import { usePolling } from "../hooks/usePolling";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export function ReviewPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const { getToken } = useAuth();
  const [svgUrl, setSvgUrl] = useState<string | null>(null);
  const [pngUrl, setPngUrl] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [regenerating, setRegenerating] = useState(false);

  // Poll for status when regenerating
  const { data: statusData } = usePolling(
    async () => {
      const token = await getToken();
      return getStatus(token, projectId!);
    },
    3000,
    regenerating
  );

  // When regeneration completes, reload design
  useEffect(() => {
    if (statusData?.design_status === "complete" && regenerating) {
      setRegenerating(false);
      loadDesign();
    }
  }, [statusData]);

  const loadDesign = async () => {
    const token = await getToken();
    const data = await getDesign(token, projectId!);
    setSvgUrl(data.svg_url);
    setPngUrl(data.png_url);
  };

  useEffect(() => {
    loadDesign();
  }, []);

  const handleSend = async (message: string, file?: File) => {
    setMessages((prev) => [...prev, { role: "user", content: message }]);

    const token = await getToken();
    const result = await sendChatMessage(token, projectId!, message, file);

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: result.response },
    ]);

    if (result.needs_regeneration) {
      setRegenerating(true);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Regenerating design..." },
      ]);
    }
  };

  // Wire up download link
  useEffect(() => {
    const link = document.getElementById("download-link") as HTMLAnchorElement;
    if (link && pngUrl) {
      link.href = pngUrl;
      link.download = "ezguilds-design.png";
    }
  }, [pngUrl]);

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
      <NavBar currentStep={3} />
      <div style={{ flex: 1, display: "flex", overflow: "hidden" }}>
        <div style={{ flex: 2 }}>
          {svgUrl ? (
            <DesignViewer svgUrl={svgUrl} />
          ) : (
            <div style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              height: "100%",
              color: "var(--text-muted)",
            }}>
              Loading design...
            </div>
          )}
        </div>
        <div style={{ flex: 1, maxWidth: "400px" }}>
          <ChatSidebar
            messages={messages}
            onSend={handleSend}
            disabled={regenerating}
          />
        </div>
      </div>
    </div>
  );
}
