from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

cliente = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

resposta = cliente.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "Diga apenas: funcionando"}
    ]
)

print(resposta.choices[0].message.content)