from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
  

class ChatResponse(BaseModel):
    message: str
    response_time: float = 0.0