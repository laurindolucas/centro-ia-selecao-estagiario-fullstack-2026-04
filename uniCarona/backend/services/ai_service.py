import os
from google import genai
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

_cache = {}


def _cache_key(dist_origem, dist_destino, diff_horario):
    return f"{round(dist_origem,1)}-{round(dist_destino,1)}-{round(diff_horario)}"


def classificar_match(dist_origem, dist_destino, diff_horario):
    key = _cache_key(dist_origem, dist_destino, diff_horario)
    if key in _cache:
        return _cache[key]

    fallback = _fallback_score(dist_origem, dist_destino, diff_horario)

    if not client:
        return fallback

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

    Retorne apenas o JSON, sem markdown.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        texto = response.text.strip().replace("```json", "").replace("```", "")
        resultado = json.loads(texto)
        _cache[key] = resultado
        return resultado

    except Exception as e:
        print(f"Erro IA: {e}")
        _cache[key] = fallback
        return fallback


def _fallback_score(dist_origem, dist_destino, diff_horario):
    score = 0
    explicacao = []

    if dist_origem <= 1:
        score += 40
        explicacao.append("origens muito próximas")
    elif dist_origem <= 3:
        score += 20
        explicacao.append("origens razoavelmente próximas")

    if dist_destino <= 1:
        score += 40
        explicacao.append("destinos muito próximos")
    elif dist_destino <= 3:
        score += 20
        explicacao.append("destinos razoavelmente próximos")

    if diff_horario <= 15:
        score += 20
        explicacao.append("horários quase idênticos")
    elif diff_horario <= 30:
        score += 10
        explicacao.append("horários compatíveis")

    if score >= 70:
        classificacao = "alta"
    elif score >= 40:
        classificacao = "média"
    else:
        classificacao = "baixa"

    texto = "Compatibilidade calculada localmente. " + (", ".join(explicacao) if explicacao else "Rotas com pouca sobreposição.")

    return {
        "classificacao": classificacao,
        "score": score,
        "explicacao": texto
    }
