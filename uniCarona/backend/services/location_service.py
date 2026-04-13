import os
from google import genai
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key) if api_key else None

geolocator = Nominatim(user_agent="unicarona_test")



def normalizar_endereco(endereco: str) -> str:
    if not client:
        return endereco

    prompt = f"""Sua tarefa é converter nomes de locais ou instituições em seus endereços completos e oficiais no Brasil.
    Se o texto for um nome (ex: "UNICAP"), retorne o endereço completo (Rua, Número, Bairro, Cidade, Estado).
    Se o texto já for um endereço, apenas padronize-o.
    Não invente dados. Se não souber, retorne o texto original.
    Retorne APENAS o endereço em uma única linha.

    Entrada: {endereco}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print(f"Erro IA: {e}")
        return endereco



def obter_coordenadas(endereco_input: str):
    try:
        endereco_limpo = normalizar_endereco(endereco_input)

        print(f"Endereço normalizado: {endereco_limpo}")

        location = geolocator.geocode(endereco_limpo, timeout=10)

        if location:
            return (location.latitude, location.longitude)

    except Exception as e:
        print(f"Erro geocoding: {e}")

    return None, None



def calcular_distancia(coord1, coord2):
    if coord1 and coord2:
        return round(geodesic(coord1, coord2).km, 2)
    return None

