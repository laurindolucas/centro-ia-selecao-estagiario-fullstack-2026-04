import os
from openai import OpenAI
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dotenv import load_dotenv

load_dotenv()

chave_api = os.getenv("GROQ_API_KEY")

cliente_ia = OpenAI(
    api_key=chave_api,
    base_url="https://api.groq.com/openai/v1"
) if chave_api else None

geolocalizador = Nominatim(user_agent="unicarona_test")


def normalizar_endereco(endereco: str) -> str:
    if not cliente_ia:
        return endereco

    prompt = f"""
            Sua tarefa é converter nomes de locais ou instituições em seus endereços completos e oficiais no Brasil.

            Regras:
            - Se for um nome (ex: "UNICAP"), retorne o endereço completo
            - Se já for um endereço, apenas padronize
            - Não invente dados
            - Se não souber, retorne o texto original

            Retorne APENAS o endereço em uma única linha.

            Entrada: {endereco}
            """

    try:
        resposta = cliente_ia.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Responda apenas com texto simples, sem explicações."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        endereco_normalizado = resposta.choices[0].message.content.strip()
        return endereco_normalizado

    except Exception as erro:
        print(f"Erro IA: {erro}")
        return endereco


def obter_coordenadas(endereco_entrada: str):
    try:
        endereco_normalizado = normalizar_endereco(endereco_entrada)

        print(f"Endereço normalizado: {endereco_normalizado}")

        local = geolocalizador.geocode(endereco_normalizado, timeout=10)

        if local:
            return (local.latitude, local.longitude)

    except Exception as erro:
        print(f"Erro geocoding: {erro}")

    return None, None


def calcular_distancia_km(coordenada1, coordenada2):
    if coordenada1 and coordenada2:
        return round(geodesic(coordenada1, coordenada2).km, 2)
    return None