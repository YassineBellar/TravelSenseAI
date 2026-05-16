const API_BASE_URL = "http://127.0.0.1:8000";
const REQUEST_TIMEOUT_MS = 30000;

export async function sendChatMessage(userMessage) {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    console.log("[CHAT DEBUG] sending to backend /chat", userMessage);

    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: userMessage }),
      signal: controller.signal,
    });

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      const detail = data?.detail || "TravelSense AI could not respond right now.";
      throw new Error(detail);
    }

    return data;
  } catch (error) {
    if (error.name === "AbortError") {
      throw new Error("TravelSense AI is taking too long to respond. Please try again.");
    }

    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}
