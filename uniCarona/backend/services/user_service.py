from database.connection import SessionLocal
from models.models import Usuario

def criar_usuario(data):
    db = SessionLocal()
    
    try:
        user = Usuario(
            nome=data.nome,
            tipo=data.tipo,
            descricao=data.descricao,
            email=data.email
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    finally:
        db.close()


def buscar_usuario(usuario_id):
    db = SessionLocal()
    try:
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()
    finally:
        db.close()

def atualizar_usuario(usuario_id, data):
    db = SessionLocal()
    
    try:
        user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
        if not user:
            return None
    
        user.nome=data.nome
        user.tipo=data.tipo
        user.descricao=data.descricao
        user.email=data.email
    
        db.commit()
        db.refresh(user)

        return user
    finally:
        db.close()


def deletar_usuario(usuario_id):
    db = SessionLocal()
    try:
        user = db.query(Usuario).filter(Usuario.id == usuario_id).first()

        if not user:
            return None

        db.delete(user)
        db.commit()

        return {"message": "Usuário deletado"}
    finally:
        db.close()