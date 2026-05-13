# TravelSense AI Project Context

This file is a handoff summary for continuing TravelSense AI in a new Codex chat.

## 1. Project Goal

TravelSense AI is an AI travel companion web app. It helps users plan, compare, and optimize trips through conversation. The product should feel like a real premium AI travel planning app, not a university demo, technical dashboard, or generic chatbot.

The core product promise:

> TravelSense AI turns scattered travel information into a clear, personalized, and reassuring travel plan.

## 2. Current Tech Stack

- Backend: Python FastAPI
- Frontend: React + Vite
- Styling: Tailwind CSS plus custom CSS utilities
- Icons: lucide-react
- Local LLM: Ollama
- Local model: qwen2.5:0.5b
- API cost: no paid API
- Streamlit: not used

## 3. Backend Status

Backend is implemented and working.

Important files:

- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/services/ollama_client.py`

Backend endpoint:

```text
POST http://127.0.0.1:8000/chat
```

Request body:

```json
{
  "message": "..."
}
```

Response body:

```json
{
  "user_message": "...",
  "assistant_response": "...",
  "provider": "ollama",
  "model": "qwen2.5:0.5b"
}
```

The frontend must display only the user-facing travel conversation, especially `assistant_response`. Do not show provider or model metadata in the UI.

## 4. Frontend Status

Frontend is implemented with React + Vite and uses the existing `/chat` endpoint.

Important files:

- `frontend/src/App.jsx`
- `frontend/src/api.js`
- `frontend/src/chatStorage.js`
- `frontend/src/useChatHistory.js`
- `frontend/src/styles.css`
- `frontend/src/components/HeroApp.jsx`
- `frontend/src/components/ChatPanel.jsx`
- `frontend/src/components/ChatHistory.jsx`
- `frontend/src/components/DestinationCards.jsx`
- `frontend/src/components/HowItWorks.jsx`
- `frontend/src/components/Reviews.jsx`
- `frontend/src/components/MobileAppPromo.jsx`
- `frontend/src/components/Footer.jsx`
- `frontend/src/components/ui.jsx`

Current homepage order:

1. Navbar inside hero
2. Hero with scenic background and centered chat-first interface
3. Destinations
4. How it works
5. Reviews
6. Mobile app promo
7. Footer

## 5. Current UI Direction

The current UI direction is:

- Premium AI travel app
- Chat-first landing screen
- Scenic travel background in the hero
- Reduced blur/gradient overlay so the image remains visible
- Minimal centered AI chat experience inspired by ChatGPT, Grok, and Perplexity
- No right-side "For You" destination panel in the first screen
- No technical dashboard layout
- Clean light sections after hero
- Rounded cards, subtle shadows, soft motion
- Travel product language only

The hero has two states:

- Pre-chat state: greeting, supporting sentence, suggestion chips, main chat input
- Active-chat state: greeting and suggestions disappear, conversation history appears, input remains visible

## 6. Color Palette

Use this palette:

- Deep Navy: `#0A1931`
- Mist Blue: `#B3CFE5`
- Ocean Blue: `#4A7FA7`
- Royal Navy: `#1A3D63`
- Snow White: `#F6FAFD`
- Optional subtle accent: Soft Sand `#E9C46A`

Rules:

- No pink.
- No random extra colors.
- Use Soft Sand only as a subtle accent if needed.
- Lower page sections should use Snow White or very light blue-tinted backgrounds.

## 7. Design Rules

- Product should look like a real premium AI travel product.
- Do not make the UI look academic, technical, or dashboard-like.
- Do not show backend or model implementation details in the UI.
- Keep hero chat as the primary focus.
- Keep scenic hero background images.
- Keep visual effects calm and not oversaturated.
- Use strong typography and generous spacing.
- Use subtle transitions and hover motion.
- Avoid "box inside box inside box" nesting.
- Keep the UI minimal, elegant, and travel-tech focused.

## 8. Current User Requirements

Latest active requirements:

- Improve chat behavior like ChatGPT/Grok.
- Long conversations must not expand the first section vertically.
- Messages should scroll inside the chat section.
- Input remains visible.
- Page layout must not grow infinitely.
- Add New Chat.
- Add saved/old chats.
- Persist conversations in `localStorage`.
- Allow switching between previous chats.
- Preserve pre-chat and active-chat behavior.
- Suggestion chips appear only before first message.
- Keep plus, attachment, voice, and send icons.
- Enter sends message.
- Shift+Enter creates a new line.
- Do not show technical metadata.

## 9. Features Already Working

Backend:

- FastAPI server
- `/chat` endpoint
- Ollama client calling `http://localhost:11434/api/generate`
- Local model fixed to `qwen2.5:0.5b`
- Basic backend error handling

Frontend:

- React + Vite app
- Tailwind styling
- Premium chat-first hero UI
- Scenic rotating hero background
- Pre-chat state
- Active-chat state
- Suggestion chips
- Message sending to `POST http://127.0.0.1:8000/chat`
- Assistant responses displayed in UI
- New Chat button
- Saved chats/history UI
- LocalStorage persistence
- Restore last active chat on reload
- Switch between saved chats
- Auto-generated chat title from first user message
- Internal message scrolling
- Input stays visible in active chat mode
- Enter sends, Shift+Enter inserts newline
- Destinations section with "Plan this trip" prompts
- How it works section
- Reviews section
- Mobile app promo with phone mockup and "Coming soon"
- Footer

## 10. Features Still Missing

Product features not implemented yet:

- Real itinerary builder UI
- Structured trip summary
- Destination comparison tables
- Budget breakdown
- Map integration
- Hotel/flight booking integrations
- User accounts/authentication
- Cloud persistence
- Delete/rename chats
- Export/share itinerary
- Real mobile app
- RAG/vector search
- Dedicated travel dataset
- Structured analysis returned by backend
- Deployment

UX improvements still useful:

- Add rename/delete chat controls.
- Add clear chat confirmation.
- Add loading skeletons for destination cards if images lag.
- Improve mobile saved chat drawer.
- Add scroll-to-current-chat polish.
- Add visual regression screenshots before final presentation.

## 11. Important Restrictions

Do not show these terms in the user-facing UI:

- Ollama
- Qwen
- LLM
- backend
- API
- provider
- model
- university project
- NLP
- RAG
- technical pipeline

Do not use:

- Streamlit
- paid APIs
- pink or fuchsia UI colors
- dashboard-style layouts
- academic labels
- raw model metadata

The backend can keep returning provider/model fields, but the frontend must ignore them.

## 12. Next Recommended Tasks

Recommended next work:

1. Add chat rename/delete actions in the saved chats panel.
2. Improve mobile chat history drawer behavior.
3. Add a compact itinerary preview after assistant responses.
4. Add a "copy response" action for assistant messages.
5. Add frontend tests or basic component smoke tests.
6. Add visual QA screenshots for desktop and mobile.
7. Prepare a presentation-ready demo script.
8. Consider a future backend route for structured trip outputs.

## Next Codex Prompt

Copy this prompt into a new Codex chat to continue:

```text
We are continuing TravelSense AI in C:\Users\Yassine\TravelSenseAI.

Please read docs/PROJECT_CONTEXT.md first. Then inspect the current frontend files.

Goal: continue improving the premium AI travel companion UI without showing technical info in the UI. Keep the backend unchanged. The frontend uses React + Vite + Tailwind and calls POST http://127.0.0.1:8000/chat. The current focus is chat-first UX with saved chats, New Chat, internal scroll, and premium minimal travel-tech design.

Next task: [replace this with the specific task].
```
