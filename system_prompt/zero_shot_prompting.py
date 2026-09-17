import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key = os.environ.get("GROQ_API_KEY"),
    base_url= "https://api.groq.com/openai/v1"
)

SYSTEM_PROMPT = "Hey, you are a helpful AI assistant who will only able to solve coding related problem. If anything is used rather than prompting just avoid those question by saying that my knowledge is limited to coding realted problems I can't give you an answer about other topics"

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages = [

        {'role': 'user', 'content': SYSTEM_PROMPT},

        {'role': 'user', 'content': "can you solve me C++ problem which will print the fibonacci numbers ?"}

        ]
            
    
)

print(response.choices[0].message.content)