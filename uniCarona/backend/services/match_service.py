from services.location_service import calcular_distancia_km
from services.ride_service import buscar_todas_rotas
from services.ai_service import classificar_compatibilidade
from services.user_service import buscar_usuario
from datetime import datetime


def calcular_diferenca_horario(h1, h2):
    formato = "%H:%M"
    t1 = datetime.strptime(h1, formato)
    t2 = datetime.strptime(h2, formato)
    return abs((t1 - t2).total_seconds() / 60)


def calcular_score(dist_origem, dist_destino, diff_horario):
    score = 0
    if dist_origem <= 1:
        score += 40
    if dist_destino <= 1:
        score += 40
    if diff_horario <= 30:
        score += 20
    return score


def encontrar_matches(rota_base):
    rotas = buscar_todas_rotas()
    resultados = []

    for rota in rotas:
        if rota.id == rota_base.id:
            continue

        if rota_base.usuario_id == rota.usuario_id:
            continue

        if rota.lat_origem is None or rota.lat_destino is None:
            continue

        dist_origem = calcular_distancia_km(
            (rota_base.lat_origem, rota_base.lon_origem),
            (rota.lat_origem, rota.lon_origem)
        )

        dist_destino = calcular_distancia_km(
            (rota_base.lat_destino, rota_base.lon_destino),
            (rota.lat_destino, rota.lon_destino)
        )

        diff_horario = calcular_diferenca_horario(
            rota_base.horario,
            rota.horario
        )

        if dist_origem is None or dist_destino is None:
            continue

        if dist_origem > 5 or dist_destino > 5:
            continue

        score = calcular_score(dist_origem, dist_destino, diff_horario)

        try:
            ia_resultado = classificar_compatibilidade(
                dist_origem,
                dist_destino,
                diff_horario
            )
        except Exception:
            ia_resultado = {
                "score": score,
                "classificacao": "média",
                "explicacao": "Erro ao processar IA"
            }

        usuario = buscar_usuario(rota.usuario_id)
        nome_usuario = usuario.nome if usuario else f"Usuário #{rota.usuario_id}"

        resultados.append({
            "rota_id": rota.id,
            "usuario_id": rota.usuario_id,
            "nome_usuario": nome_usuario,
            "origem": rota.origem,
            "destino": rota.destino,
            "horario": rota.horario,
            "dist_origem_km": dist_origem,
            "dist_destino_km": dist_destino,
            "diferenca_horario_min": diff_horario,
            "score_backend": score,
            "score_ia": ia_resultado["score"],
            "classificacao": ia_resultado["classificacao"],
            "explicacao": ia_resultado["explicacao"],
        })

    resultados.sort(key=lambda x: x["score_ia"], reverse=True)
    return resultados[:5]
