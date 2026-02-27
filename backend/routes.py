import logging
from fastapi import APIRouter
from fastapi import HTTPException
from backend.schemas import ChatRequest, ChatResponse
from backend.tools import get_last_chart, clear_last_chart

_agent_executor = None
logger = logging.getLogger(__name__)


def set_agent(agent_executor) -> None:
    global _agent_executor
    _agent_executor = agent_executor


router = APIRouter(prefix="/api", tags=["chat"])


def _build_fallback_message(error: Exception) -> str:
    error_text = str(error).strip()
    error_lower = error_text.lower()

    if "rate limit" in error_lower or "429" in error_lower:
        return (
            "The model provider is rate-limiting requests right now. "
            "Please retry in a few seconds."
        )

    if "api key" in error_lower or "authentication" in error_lower:
        return (
            "The model provider rejected authentication. Please verify API credentials."
        )

    if "max iterations" in error_lower:
        return (
            "I could not complete that request in time. "
            "Try rephrasing it in a shorter, more specific way."
        )

    if error_text:
        return f"I couldn't process that question right now: {error_text}"

    return "I couldn't process that question right now. Please try again."


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    if _agent_executor is None:
        raise HTTPException(
            status_code=500,
            detail="Agent not initialized. Please restart the server.",
        )

    try:
        clear_last_chart()

        result = _agent_executor.invoke({"input": request.message})
        if isinstance(result, dict):
            text_response = result.get("output", "I couldn't generate a response.")
        else:
            text_response = str(result)

        visualization = get_last_chart()

        return ChatResponse(
            text_response=text_response,
            visualization=visualization,
        )

    except Exception as e:
        logger.exception("Error while handling /api/chat")
        return ChatResponse(
            text_response=_build_fallback_message(e),
            visualization=None,
        )
