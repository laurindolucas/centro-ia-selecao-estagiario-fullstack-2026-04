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
    Converta o local em um endereço oficial do Brasil.
    Exemplo 1: "UNICAP" -> "Rua do Príncipe, 526, Boa Vista, Recife - PE"
    Exemplo 2: "Rua 15 de nov, 10, SP" -> "Rua Quinze de Novembro, 10, São Paulo - SP"
    
    Regras:
    - Retorne APENAS o endereço.
    - Se não souber, repita exatamente o texto de entrada.
    - PROIBIDO dar explicações ou saudações.

    Entrada: {endereco}
    """

    try:
        resposta = cliente_ia.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Você é um assistente que retorna apenas endereços puros, sem conversas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1 
        )

        resultado = resposta.choices[0].message.content.strip()
        
        palavras_negativas = ["infelizmente", "desculpe", "não posso", "como um modelo"]
        if any(palavra in resultado.lower() for palavra in palavras_negativas) or len(resultado) > 150:
            print(f"Alerta: IA retornou lixo, ignorando normalização.")
            return endereco
            
        return resultado

    except Exception as erro:
        print(f"Erro IA: {erro}")
        return endereco

def obter_coordenadas(endereco_entrada: str):
    try:
        endereco_para_buscar = normalizar_endereco(endereco_entrada)
        print(f"Buscando: {endereco_para_buscar}")

        local = geolocalizador.geocode(endereco_para_buscar, timeout=10)
        if not local and endereco_para_buscar != endereco_entrada:
            print("IA falhou em gerar endereço válido, tentando original...")
            local = geolocalizador.geocode(endereco_entrada, timeout=10)

        if local:
            return (local.latitude, local.longitude)

    except Exception as erro:
        print(f"Erro geocoding: {erro}")

    return None, None

def calcular_distancia_km(coordenada1, coordenada2):
    if coordenada1 and coordenada2:
        try:
            return round(geodesic(coordenada1, coordenada2).km, 2)
        except Exception:
            return None
    return None