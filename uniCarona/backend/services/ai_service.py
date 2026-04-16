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

    prompt = f"""Você é um especialista em logística urbana e sistemas de mobilidade inteligente.
        Sua tarefa é avaliar a viabilidade de uma carona compartilhada entre dois universitários.

        Dados técnicos:
        - Desvio na origem: {dist_origem} km
        - Desvio no destino: {dist_destino} km
        - Janela temporal (diferença de horário): {diferenca_horario} minutos

        Regras de Negócio:
        - Priorize a convergência de trajeto (distâncias baixas).
        - A janela temporal ideal é inferior a 30 minutos.
        - O score deve refletir a eficiência logística (0 a 100).

        Instruções de Resposta:
        1. A "explicacao" deve ser amigável e didática, porém profissional. Use termos técnicos como "convergência de trajeto" ou "janela temporal", mas explique de forma "suave" como se estivesse conversando com o usuário.
        2. A "explicacao" DEVE começar obrigatoriamente com o prefixo "[IA] Sugestão: ".
        3. Retorne APENAS o JSON solicitado.

        Formato:
        {{
        "classificacao": "alta | média | baixa",
        "score": número,
        "explicacao": "[IA] Sugestão: Texto técnico porém suave aqui..."
        }}
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