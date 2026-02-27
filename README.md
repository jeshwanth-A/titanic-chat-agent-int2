# Titanic Chat Agent

A production-ready chatbot project that answers questions about Titanic passenger data and generates visualizations.

## Tech stack

- Backend: FastAPI
- Agent framework: LangChain
- Frontend: Streamlit
- LLM provider: Groq

## Project structure

```text
backend/
frontend/
data/
requirements.txt
```

## 1) Local setup

1. Create and activate a virtual environment.
2. Install dependencies.
3. Copy `.env.example` to `.env` and add your key.

```bash
pip install -r requirements.txt
```

## 2) Run locally

Start backend (terminal 1):

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Start frontend (terminal 2):

```bash
streamlit run frontend/app.py
```

Optional frontend env var (if backend is not on default localhost:8000):

```bash
BACKEND_URL=http://localhost:8000
```

## 3) Deploy backend on Render

Create a new Web Service from this repo and configure:

- Root directory: (leave empty)
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

Set environment variable in Render:

- `GROQ_API_KEY=<your_groq_api_key>`

After deploy, copy the Render URL, for example:

`https://your-backend-name.onrender.com`

## 4) Deploy frontend on Streamlit Community Cloud

Create app from GitHub repo with:

- Main file path: `frontend/app.py`


In Streamlit app settings -> Secrets, add:

```toml
BACKEND_URL = "https://your-backend-name.onrender.com"
```

## Security notes

- Never commit `.env`.
- Keep `GROQ_API_KEY` only in local `.env` and deployment platform secrets.
- The reviewer can test only using the Streamlit URL. They do not need your API key.
