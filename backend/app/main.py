import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

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
USE_RAG = True
RAG_TIMEOUT_SECONDS = 0.1
_rag_executor = ThreadPoolExecutor(max_workers=1)

try:
    from services.rag_retriever import get_last_match_counts, load_rag_data, retrieve_travel_context
except ImportError:
    from backend.services.rag_retriever import (
        get_last_match_counts,
        load_rag_data,
        retrieve_travel_context,
    )

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


@app.on_event("startup")
def startup() -> None:
    """Warm the tiny CSV cache once so requests only do in-memory matching."""

    if USE_RAG:
        try:
            load_rag_data()
            if DEBUG_LOGS:
                print("[RAG DEBUG] CSV cache loaded at startup")
        except Exception as exc:
            if DEBUG_LOGS:
                print("[RAG DEBUG] startup load failed:", str(exc))


@app.get("/")
def root() -> dict[str, str]:
    """Simple health route for quick browser checks."""

    return {"message": "TravelSense AI backend is running."}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """Send a TravelSense prompt to the local model and return a user-facing response."""

    request_start = time.perf_counter()

    def log_timing(step: str) -> None:
        if DEBUG_LOGS:
            elapsed_ms = (time.perf_counter() - request_start) * 1000
            print(f"[TIMING] {step}: {elapsed_ms:.1f}ms")

    try:
        log_timing("start request")
        user_message = request.message
        print("🔥 ACTIVE /chat CALLED:", user_message)
        log_timing("after reading user_message")

        analysis = analyze_message(user_message)
        log_timing("after analyze_message()")

        if DEBUG_LOGS:
            print("[DEBUG] received:", user_message)
            print("[TravelSense DEBUG] received user message:", user_message)
            print("[TravelSense DEBUG] analysis.language:", analysis.language)
            print("[TravelSense DEBUG] analysis.intent:", analysis.intent)
            print("[TravelSense DEBUG] analysis.emotion:", analysis.emotion)
            print("[TravelSense DEBUG] analysis.entities:", analysis.entities)
            print("[TravelSense DEBUG] analysis.missing_context:", analysis.missing_context)

        rag_context = ""
        rag_start = time.perf_counter()
        if USE_RAG:
            try:
                future = _rag_executor.submit(retrieve_travel_context, user_message, analysis)
                rag_context = future.result(timeout=RAG_TIMEOUT_SECONDS)
            except TimeoutError:
                rag_context = ""
                if DEBUG_LOGS:
                    print("[RAG DEBUG] skipped: retrieval timed out")
            except Exception as exc:
                rag_context = ""
                if DEBUG_LOGS:
                    print("[RAG DEBUG] skipped: retrieval failed:", str(exc))
        else:
            if DEBUG_LOGS:
                print("[RAG DEBUG] disabled by USE_RAG=False")

        rag_duration_ms = (time.perf_counter() - rag_start) * 1000
        print("[RAG] USE_RAG:", USE_RAG)
        print("[RAG] context length:", len(rag_context))
        log_timing("after retrieve_travel_context()")

        if DEBUG_LOGS:
            destination_catalog_matched = "Destination context:" in rag_context
            articles_rag_matched = "Travel guide context:" in rag_context
            match_counts = get_last_match_counts() if USE_RAG else {"destinations": 0, "articles": 0}

            print("[CHAT DEBUG] user_message:", user_message)
            print("[CHAT DEBUG] analysis:", analysis)
            print("[CHAT DEBUG] USE_RAG:", USE_RAG)
            print("[RAG DEBUG] rag_context length:", len(rag_context))
            print("[RAG DEBUG] rag_context preview:", rag_context[:300])
            print("[RAG DEBUG] matched destination rows:", match_counts["destinations"])
            print("[RAG DEBUG] matched article rows:", match_counts["articles"])
            print("[RAG DEBUG] user_message:", user_message)
            print("[RAG DEBUG] analysis.entities:", analysis.entities)
            print("[RAG DEBUG] USE_RAG:", USE_RAG)
            print(f"[RAG DEBUG] retrieval_duration_ms: {rag_duration_ms:.1f}")
            print("[RAG DEBUG] rag_context_length:", len(rag_context))
            print("[RAG DEBUG] rag_context_preview:", rag_context[:300])
            print("[RAG DEBUG] matched_destination_rows_count:", match_counts["destinations"])
            print("[RAG DEBUG] matched_article_rows_count:", match_counts["articles"])
            print("[RAG DEBUG] destinations_catalog_matched:", destination_catalog_matched)
            print("[RAG DEBUG] articles_tourism_rag_matched:", articles_rag_matched)
            print("[TravelSense DEBUG] rag_context_chars:", len(rag_context))
            print("[DEBUG] before prompt build")

        prompt = build_travelsense_prompt(user_message, rag_context)
        log_timing("after build_travelsense_prompt()")

        if DEBUG_LOGS:
            print("[DEBUG] before ollama call")
            print("[TravelSense DEBUG] before calling Ollama")
        log_timing("before Ollama call")

        raw_response = ollama_client.generate(prompt)
        log_timing("after Ollama call")

        if DEBUG_LOGS:
            print("[DEBUG] after ollama call")
            print("[TravelSense DEBUG] after receiving Ollama response")

        assistant_response = clean_assistant_response(raw_response)
        log_timing("after clean_assistant_response()")

        fallback_reason = get_fallback_reason(assistant_response, analysis)
        if DEBUG_LOGS:
            print("[TravelSense DEBUG] fallback_triggered:", fallback_reason is not None)
            print("[TravelSense DEBUG] fallback_reason:", fallback_reason)

        assistant_response = ensure_response_quality(assistant_response, analysis)
    except OllamaClientError as exc:
        log_timing("Ollama error")
        if DEBUG_LOGS:
            print("[TravelSense DEBUG] Ollama error:", str(exc))

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="TravelSense AI could not respond right now. Please try again in a moment.",
        ) from exc

    response = ChatResponse(
        user_message=request.message,
        assistant_response=assistant_response,
        provider=OLLAMA_PROVIDER,
        model=OLLAMA_MODEL,
    )
    log_timing("final response returned")
    return response
