# TravelSense AI

TravelSense AI is an AI travel companion web app. It helps users plan, compare, and optimize trips through conversation.

The app uses a local FastAPI backend with Ollama and a React + Vite frontend. There is no paid API and no Streamlit app.


## Requirements

- Python 3.10+
- Node.js 20+
- Ollama installed locally
- Ollama model: `qwen2.5:0.5b`

## Run Ollama

```powershell
ollama serve
ollama pull qwen2.5:0.5b
```

Optional quick test:

```powershell
python test_ollama.py
```

## Run Backend

From the project root:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Test `/chat`:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/chat" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"message":"Plan a simple 3-day trip to Paris."}'
```

## Run Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## Project Structure

```text
TravelSenseAI/
  backend/
    app/
      main.py
      models.py
      services/
        ollama_client.py
  docs/
    PROJECT_CONTEXT.md
  frontend/
    src/
      App.jsx
      api.js
      chatStorage.js
      useChatHistory.js
      components/
        ChatHistory.jsx
        ChatPanel.jsx
        HeroApp.jsx
        DestinationCards.jsx
        HowItWorks.jsx
        Reviews.jsx
        MobileAppPromo.jsx
        Footer.jsx
  requirements.txt
  test_ollama.py
```
