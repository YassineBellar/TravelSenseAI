import os

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .models import ChatRequest, ChatResponse
from .services.ollama_client import OllamaClient, OllamaClientError
from .services.prompt_builder import (
    analyze_message,
    build_travelsense_prompt,
    clean_assistant_response,
    ensure_response_quality,
    get_fallback_reason,
)


OLLAMA_PROVIDER = "ollama"
OLLAMA_MODEL = "qwen2.5:0.5b"
DEBUG_LOGS = os.getenv("TRAVELSENSE_DEBUG", "1") == "1"

app = FastAPI(
    title="TravelSense AI API",
    description="Local LLM backend for the TravelSense AI university project.",
    version="0.1.0",
)

# Kept ready for the future React + Vite frontend during local development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ollama_client = OllamaClient(model=OLLAMA_MODEL)


@app.get("/")
def root() -> dict[str, str]:
    """Simple health route for quick browser checks."""

    return {"message": "TravelSense AI backend is running."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Send a TravelSense prompt to the local model and return a user-facing response."""

    try:
        user_message = request.message
        analysis = analyze_message(user_message)
        if DEBUG_LOGS:
            print("[TravelSense DEBUG] user_message:", user_message)
            print("[TravelSense DEBUG] analysis.language:", analysis.language)
            print("[TravelSense DEBUG] analysis.intent:", analysis.intent)
            print("[TravelSense DEBUG] analysis.emotion:", analysis.emotion)
            print("[TravelSense DEBUG] analysis.entities:", analysis.entities)
            print("[TravelSense DEBUG] analysis.missing_context:", analysis.missing_context)

        prompt = build_travelsense_prompt(user_message)
        assistant_response = clean_assistant_response(ollama_client.generate(prompt))
        fallback_reason = get_fallback_reason(assistant_response, analysis)
        if DEBUG_LOGS:
            print("[TravelSense DEBUG] fallback_triggered:", fallback_reason is not None)
            print("[TravelSense DEBUG] fallback_reason:", fallback_reason)

        assistant_response = ensure_response_quality(assistant_response, analysis)
    except OllamaClientError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return ChatResponse(
        user_message=request.message,
        assistant_response=assistant_response,
        provider=OLLAMA_PROVIDER,
        model=OLLAMA_MODEL,
    )
