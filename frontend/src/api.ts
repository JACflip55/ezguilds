const BASE = "/api";

async function request(
  path: string,
  token: string,
  options: RequestInit = {}
): Promise<Response> {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res;
}

export async function createProject(token: string) {
  const res = await request("/projects", token, { method: "POST" });
  return res.json();
}

export async function uploadFile(
  token: string,
  projectId: string,
  file: File,
  fileType: string
) {
  const form = new FormData();
  form.append("file", file);
  form.append("file_type", fileType);
  const res = await request(`/projects/${projectId}/upload`, token, {
    method: "POST",
    body: form,
  });
  return res.json();
}

export async function getNextQuestion(token: string, projectId: string) {
  const res = await request(`/projects/${projectId}/questions`, token);
  return res.json();
}

export async function submitAnswer(
  token: string,
  projectId: string,
  answer: string
) {
  const res = await request(`/projects/${projectId}/answers`, token, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ answer }),
  });
  return res.json();
}

export async function startGeneration(token: string, projectId: string) {
  const res = await request(`/projects/${projectId}/generate`, token, {
    method: "POST",
  });
  return res.json();
}

export async function getStatus(token: string, projectId: string) {
  const res = await request(`/projects/${projectId}/status`, token);
  return res.json();
}

export async function getDesign(token: string, projectId: string) {
  const res = await request(`/projects/${projectId}/design`, token);
  return res.json();
}

export async function sendChatMessage(
  token: string,
  projectId: string,
  message: string,
  file?: File
) {
  const form = new FormData();
  form.append("message", message);
  if (file) form.append("file", file);
  const res = await request(`/projects/${projectId}/chat`, token, {
    method: "POST",
    body: form,
  });
  return res.json();
}
