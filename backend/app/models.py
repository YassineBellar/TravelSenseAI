from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request body for the chat endpoint."""

    message: str = Field(..., min_length=1, description="User message to send to the local LLM.")


class ChatResponse(BaseModel):
    """Stable API response returned by /chat."""

    user_message: str
    assistant_response: str
    provider: str
    model: str
