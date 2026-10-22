from fastapi import FastAPI
from ollama_route import router as ollama_router

app = FastAPI()

app.include_router(ollama_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}