from fastapi import APIRouter
from schemas.schemas import RideCreate
from services.ride_service import (
    criar_rota,
    buscar_todas_rotas,
    atualizar_rota,
    deletar_rota,
    buscar_rota_por_id
)

router = APIRouter()

@router.post("/rotas")
def criar_rotas_rota(rota: RideCreate):
    return criar_rota(rota)

@router.get("/rotas")
def buscar_todas_rotas_rota():
    return buscar_todas_rotas()

@router.get("/rotas/{rota_id}")
def buscar_rota_por_id_rota(rota_id: int):
    return buscar_rota_por_id(rota_id)

@router.put("/rotas/{rotas_id}")
def atulizar_rotas_rota(rotas_id: int, rota: RideCreate):
    return atualizar_rota()

@router.delete("/rotas/{rotas_id}")
def deletar_rotas_rota(rotas_id: int):
    return deletar_rota(rotas_id)