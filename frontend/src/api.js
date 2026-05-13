const API_BASE_URL = "http://127.0.0.1:8000";

export async function sendChatMessage(message) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }),
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = data?.detail || "The planner could not process this message.";
    throw new Error(detail);
  }

  return data;
}
