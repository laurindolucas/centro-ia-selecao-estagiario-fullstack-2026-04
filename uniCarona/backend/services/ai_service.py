import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

load_dotenv()

chave_api = os.getenv("GROQ_API_KEY")

cliente_ia = OpenAI(
    api_key=chave_api,
    base_url="https://api.groq.com/openai/v1"
) if chave_api else None

cache_resultados = {}


def gerar_chave_cache(dist_origem, dist_destino, diferenca_horario):
    return f"{round(dist_origem,1)}-{round(dist_destino,1)}-{round(diferenca_horario)}"


def classificar_compatibilidade(dist_origem, dist_destino, diferenca_horario):
    chave = gerar_chave_cache(dist_origem, dist_destino, diferenca_horario)

    if chave in cache_resultados:
        return cache_resultados[chave]

    resultado_fallback = calcular_compatibilidade_local(
        dist_origem, dist_destino, diferenca_horario
    )

    if not cliente_ia:
        return resultado_fallback

    prompt = f"""
        Você é um sistema de recomendação de caronas.

        Analise os dados abaixo e avalie a compatibilidade entre duas rotas.

        Dados:
        - Distância entre origens: {dist_origem} km
        - Distância entre destinos: {dist_destino} km
        - Diferença de horário: {diferenca_horario} minutos

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
        resposta = cliente_ia.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Responda apenas com JSON válido."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        texto_resposta = resposta.choices[0].message.content.strip()

        json_encontrado = re.search(r"\{.*\}", texto_resposta, re.DOTALL)
        if not json_encontrado:
            raise ValueError("Resposta inválida da IA")

        resultado = json.loads(json_encontrado.group())

        cache_resultados[chave] = resultado
        return resultado

    except Exception as erro:
        print(f"Erro IA: {erro}")
        cache_resultados[chave] = resultado_fallback
        return resultado_fallback


def calcular_compatibilidade_local(dist_origem, dist_destino, diferenca_horario):
    score = 0
    explicacoes = []

    if dist_origem <= 1:
        score += 40
        explicacoes.append("origens muito próximas")
    elif dist_origem <= 3:
        score += 20
        explicacoes.append("origens razoavelmente próximas")
    if dist_destino <= 1:
        score += 40
        explicacoes.append("destinos muito próximos")
    elif dist_destino <= 3:
        score += 20
        explicacoes.append("destinos razoavelmente próximos")

    if diferenca_horario <= 15:
        score += 20
        explicacoes.append("horários quase idênticos")
    elif diferenca_horario <= 30:
        score += 10
        explicacoes.append("horários compatíveis")

    if score >= 70:
        classificacao = "alta"
    elif score >= 40:
        classificacao = "média"
    else:
        classificacao = "baixa"

    explicacao_final = (
        "Compatibilidade calculada localmente. "
        + (", ".join(explicacoes) if explicacoes else "Rotas com pouca sobreposição.")
    )

    return {
        "classificacao": classificacao,
        "score": score,
        "explicacao": explicacao_final
    }