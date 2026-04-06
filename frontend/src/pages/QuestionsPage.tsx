import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import { NavBar } from "../components/NavBar";
import { getNextQuestion, submitAnswer, startGeneration } from "../api";

interface AnswerEntry {
  question: string;
  answer: string;
}

export function QuestionsPage() {
  const { projectId } = useParams<{ projectId: string }>();
  const { getToken } = useAuth();
  const navigate = useNavigate();

  const [currentQuestion, setCurrentQuestion] = useState<{
    question: string;
    why: string;
  } | null>(null);
  const [answerText, setAnswerText] = useState("");
  const [previousAnswers, setPreviousAnswers] = useState<AnswerEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [questionNumber, setQuestionNumber] = useState(1);

  const fetchQuestion = async () => {
    setLoading(true);
    const token = await getToken();
    const result = await getNextQuestion(token, projectId!);
    setCurrentQuestion(result);
    setLoading(false);
  };

  useEffect(() => {
    fetchQuestion();
  }, []);

  const handleSubmit = async () => {
    if (!answerText.trim() || !currentQuestion) return;
    setSubmitting(true);
    const token = await getToken();
    await submitAnswer(token, projectId!, answerText);
    setPreviousAnswers((prev) => [
      ...prev,
      { question: currentQuestion.question, answer: answerText },
    ]);
    setAnswerText("");
    setQuestionNumber((n) => n + 1);
    setSubmitting(false);
    fetchQuestion();
  };

  const handleSkip = async () => {
    const token = await getToken();
    await startGeneration(token, projectId!);
    navigate(`/project/${projectId}/generating`);
  };

  return (
    <div>
      <NavBar currentStep={1} />
      <div style={{ maxWidth: "640px", margin: "2rem auto", padding: "0 1.5rem" }}>
        <p style={{
          fontSize: "0.75rem",
          color: "var(--text-faint)",
          marginBottom: "1rem",
        }}>
          Question {questionNumber} · Answer as many as you'd like
        </p>

        {loading ? (
          <p style={{ color: "var(--text-muted)" }}>Generating question...</p>
        ) : currentQuestion ? (
          <>
            <div style={{
              background: "var(--bg-elevated)",
              border: "1px solid var(--border-light)",
              borderRadius: "8px",
              padding: "1.25rem",
              marginBottom: "1rem",
            }}>
              <h3 style={{ fontSize: "1rem", marginBottom: "0.5rem" }}>
                {currentQuestion.question}
              </h3>
              <p style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>
                {currentQuestion.why}
              </p>
            </div>

            <textarea
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Type your answer..."
              style={{
                width: "100%",
                minHeight: "80px",
                marginBottom: "1rem",
                resize: "vertical",
              }}
            />

            <div style={{ display: "flex", gap: "0.75rem" }}>
              <button
                onClick={handleSubmit}
                disabled={submitting || !answerText.trim()}
                style={{
                  flex: 1,
                  opacity: answerText.trim() ? 1 : 0.4,
                }}
              >
                {submitting ? "Submitting..." : "Submit Answer →"}
              </button>
              <button
                onClick={handleSkip}
                style={{
                  background: "transparent",
                  border: "1px solid var(--border)",
                  color: "var(--text-muted)",
                  whiteSpace: "nowrap",
                }}
              >
                Skip to Design ⏭
              </button>
            </div>
          </>
        ) : null}

        {previousAnswers.length > 0 && (
          <div style={{
            marginTop: "1.5rem",
            fontSize: "0.8rem",
            color: "var(--text-faint)",
          }}>
            <p style={{ marginBottom: "0.5rem" }}>Previously answered:</p>
            {previousAnswers.map((a, i) => (
              <p key={i}>
                {i + 1}. {a.question}: {a.answer}
              </p>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
