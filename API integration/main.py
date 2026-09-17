import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI(
    api_key = os.environ.get("GROQ_API_KEY"),
    base_url= "https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="qwen/qwen3.8-27b",
    messages = [
        {
            'role': 'user',
            'content': 'Hi there !'
        }
    ]

    
)

print(response.choices[0].message.content)