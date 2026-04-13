import os
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


def classificar_match(dist_origem, dist_destino, diff_horario):
    if not client:
        return {
            "classificacao": "média",
            "score": 50,
            "explicacao": "IA indisponível"
        }

    prompt = f"""
    Você é um sistema de recomendação de caronas.

    Analise os dados abaixo e avalie a compatibilidade entre duas rotas.

    Dados:
    - Distância entre origens: {dist_origem} km
    - Distância entre destinos: {dist_destino} km
    - Diferença de horário: {diff_horario} minutos

    Regras:
    - Distâncias menores indicam melhor compatibilidade
    - Diferença de horário menor que 30 minutos é ideal

    Retorne um JSON no formato:

    {{
      "classificacao": "alta | média | baixa",
      "score": número de 0 a 100,
      "explicacao": "Texto curto explicando a decisão"
    }}

    Retorne apenas o JSON.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        texto = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(texto)

    except Exception as e:
        print(f"Erro IA: {e}")
        return {
            "classificacao": "média",
            "score": 50,
            "explicacao": "Erro ao processar IA"
        }