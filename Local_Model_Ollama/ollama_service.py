# from ollama import Ollama
from time import time
from unittest import result

from ollama import Client

client = Client(
    host="http://localhost:11434"
)

MODEL_NAME = "qwen2.5:3b"

SYSTEM_PROMPT = """You are a helpful assistant. You will answer the user's questions to the best of your ability. If you don't know the answer, you will say "I don't know"."""

def response(message:str) -> dict[str, float]:
    start_time = time()
    result = client.chat(
        model = MODEL_NAME,
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],

        options = {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 400,
            "num_ctx": 2048,
            "num_thread": 6,
        }

    )

    end_time = time()
    response_time = end_time - start_time

    return {

        "message": result["message"]["content"], 
        "response_time": response_time
        
          }

