import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

payload = {
    "model": "qwen2.5:0.5b",
    "prompt": "You are TravelSense AI. Help me plan a 5-day cultural trip with a medium budget.",
    "stream": False,
}

try:
    response = requests.post(OLLAMA_URL, json=payload, timeout=60)

    print("Status code:", response.status_code)
    print("Raw response:")
    print(response.text)

    response.raise_for_status()

    data = response.json()
    print("\nOllama response:")
    print(data.get("response", "No response found"))

except requests.exceptions.ConnectionError:
    print("Error: Ollama is not running. Open Ollama or run: ollama serve")

except Exception as exc:
    print("Error:", exc)
