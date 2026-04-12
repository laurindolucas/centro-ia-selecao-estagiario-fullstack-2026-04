from database.connection import SessionLocal
from models.models import Usuario

def create_user(data):
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


def get_user(user_id):
    db = SessionLocal()
    try:
        return db.query(Usuario).filter(Usuario.id == user_id).first()
    finally:
        db.close()

def update_user(user_id, data):
    db = SessionLocal()
    
    try:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
    
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


def delete_user(user_id):
    db = SessionLocal()
    try:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()

        if not user:
            return None

        db.delete(user)
        db.commit()

        return {"message": "Usuário deletado"}
    finally:
        db.close()