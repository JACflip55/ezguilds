import { useState, useRef } from "react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface ChatSidebarProps {
  messages: Message[];
  onSend: (message: string, file?: File) => Promise<void>;
  disabled?: boolean;
}

export function ChatSidebar({ messages, onSend, disabled }: ChatSidebarProps) {
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleSend = async () => {
    if (!input.trim() || sending) return;
    setSending(true);
    await onSend(input.trim());
    setInput("");
    setSending(false);
  };

  const handleFileUpload = () => {
    fileRef.current?.click();
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSending(true);
      await onSend(`[Uploaded: ${file.name}]`, file);
      setSending(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100%",
      borderLeft: "1px solid var(--border-light)",
      fontSize: "0.85rem",
    }}>
      <div style={{
        padding: "0.75rem",
        borderBottom: "1px solid var(--border-light)",
        fontWeight: 600,
        color: "var(--accent-green-heading)",
      }}>
        Chat
      </div>

      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "0.75rem",
        display: "flex",
        flexDirection: "column",
        gap: "0.5rem",
      }}>
        {messages.map((m, i) => (
          <div key={i} style={{
            background: m.role === "assistant"
              ? "rgba(100,130,70,0.12)"
              : "rgba(255,255,255,0.04)",
            borderRadius: "6px",
            padding: "0.5rem",
          }}>
            <p style={{ color: "var(--text-faint)", fontSize: "0.7rem" }}>
              {m.role === "user" ? "You" : "EZGuilds"}
            </p>
            <p>{m.content}</p>
          </div>
        ))}
      </div>

      <div style={{
        padding: "0.5rem",
        borderTop: "1px solid var(--border-light)",
        display: "flex",
        gap: "0.5rem",
      }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask for changes..."
          disabled={disabled || sending}
          style={{ flex: 1 }}
        />
        <button
          onClick={handleSend}
          disabled={disabled || sending || !input.trim()}
          style={{ padding: "0.4rem 0.75rem" }}
        >
          Send
        </button>
      </div>

      <div style={{
        padding: "0.5rem",
        borderTop: "1px solid var(--border-light)",
        display: "flex",
        gap: "0.5rem",
      }}>
        <input
          ref={fileRef}
          type="file"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
        <button
          onClick={handleFileUpload}
          style={{
            flex: 1,
            background: "transparent",
            border: "1px solid var(--border)",
            color: "var(--text-muted)",
            fontSize: "0.75rem",
          }}
        >
          Upload
        </button>
        <a
          href="#"
          id="download-link"
          style={{
            flex: 1,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            background: "transparent",
            border: "1px solid var(--border)",
            borderRadius: "6px",
            color: "var(--text-muted)",
            fontSize: "0.75rem",
            textDecoration: "none",
          }}
        >
          Download PNG
        </a>
      </div>
    </div>
  );
}
