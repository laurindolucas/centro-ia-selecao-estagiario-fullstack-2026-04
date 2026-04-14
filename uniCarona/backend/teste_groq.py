from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

resposta = cliente.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Me diga oi"}
    ]
)

print(resposta.choices[0].message.content)