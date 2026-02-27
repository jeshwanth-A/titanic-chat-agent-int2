from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.data_loader import load_titanic_data
from backend.tools import set_dataframe
from backend.agent import create_agent
from backend.routes import router, set_agent
from backend.config import FASTAPI_HOST, FASTAPI_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading Titanic dataset...")
    df = load_titanic_data()
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    set_dataframe(df)
    print("DataFrame set in tools module")

    print("Creating LangChain agent with Groq LLM...")
    agent_executor = create_agent(df)
    print("Agent created successfully")

    set_agent(agent_executor)
    print("Agent registered with routes")

    print("=" * 50)
    print(f"Server is ready at http://localhost:{FASTAPI_PORT}")
    print(f"API docs at http://localhost:{FASTAPI_PORT}/docs")
    print("=" * 50)

    yield

    print("Server shutting down...")


app = FastAPI(
    title="Titanic Chat Agent API",
    description="A chatbot that analyzes the Titanic dataset using natural language. "
    "Ask questions about passengers, survival rates, and more!",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Titanic Chat Agent API is running!",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=FASTAPI_HOST,
        port=FASTAPI_PORT,
        reload=True,
    )
