from fastapi import APIRouter
from services.match_service import encontrar_matches
from services.ride_service import buscar_rota_por_id

router = APIRouter()


@router.get("/matches/{rota_id}")
def buscar_matches(rota_id: int):
    rota = buscar_rota_por_id(rota_id)

    if not rota:
        return {"erro": "Rota não encontrada"}

    return encontrar_matches(rota)