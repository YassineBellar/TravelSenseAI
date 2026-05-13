import requests


class OllamaClientError(RuntimeError):
    """Raised when the backend cannot get a valid response from Ollama."""


class OllamaClient:
    """Small client for Ollama's local generate API."""

    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "qwen2.5:0.5b",
        timeout_seconds: int = 60,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def generate(self, prompt: str, options: dict | None = None) -> str:
        """Send a prompt to Ollama and return the generated text."""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": options or _default_generation_options(),
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            raise OllamaClientError(
                "Could not reach Ollama. Make sure it is running on http://localhost:11434."
            ) from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise OllamaClientError("Ollama returned a response that was not valid JSON.") from exc

        assistant_response = data.get("response")

        if not assistant_response:
            raise OllamaClientError("Ollama returned an empty response.")

        return assistant_response.strip()


def _default_generation_options() -> dict:
    """Stable defaults for concise travel answers from a small local model."""

    return {
        "temperature": 0.35,
        "top_p": 0.85,
        "top_k": 40,
        "repeat_penalty": 1.15,
        "num_ctx": 2048,
        "num_predict": 300,
        "stop": [
            "\nUser:",
            "\nUtilisateur:",
            "\nSystem:",
            "\nSystème:",
        ],
    }
