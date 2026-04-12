from fastapi import APIRouter
from schemas.schemas import UserCreate
from services.user_service import (
    criar_usuario,
    buscar_usuario,
    atualizar_usuario,
    deletar_usuario
)

router = APIRouter()

@router.post("/users")
def criar_usuario_rota(user: UserCreate):
    return criar_usuario(user)


@router.get("/users/{usuario_id}")
def buscar_usuario_rota(usuario_id: int):
    return buscar_usuario(usuario_id)


@router.put("/users/{usuario_id}")
def atualizar_usuario_rota(usuario_id: int, user: UserCreate):
    return atualizar_usuario(usuario_id, user)


@router.delete("/users/{usuario_id}")
def deletar_usuario_rota(usuario_id: int):
    return deletar_usuario(usuario_id)