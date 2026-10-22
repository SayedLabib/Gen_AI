from fastapi import APIRouter


from ollama_schema import ChatRequest, ChatResponse
from ollama_service import response

router = APIRouter(
    prefix="/ollama",
    tags=["ollama"]
)


@router.post("/chat", response_model=ChatResponse)

async def chat(request: ChatRequest):
    reply = response(request.message)
    return ChatResponse(message=reply["message"], response_time=reply["response_time"])