from database.connection import SessionLocal
from models.models import Rota

def criar_rota(data):
    db = SessionLocal()
    
    try:
        rota = Rota(
           usuario_id=data.usuario_id,
           origem = data.origem,
           destino = data.destino,
           horario = data.horario 
        )
        
        db.add(rota)
        db.commit()
        db.refresh(rota)
        
        return rota
    finally:
        db.close()
        
def buscar_todas_rotas():
    db = SessionLocal()
    try:
        return db.query(Rota).all()
    finally:
        db.close()

def atualizar_rota(rota_id, data):
    db = SessionLocal()
    
    try:
        rota = db.query(Rota).filter(Rota.id == rota_id).first()
        
        if not rota:
            return {"message": "Rota não encontrada!"}
        
        rota.origem = data.origem
        rota.destino = data.destino
        rota.horario = data.horario
        
        db.commit()
        db.refresh(rota)
        
        return rota
    finally:
        db.close()
        
        
def deletar_rota(rota_id):
    db = SessionLocal()
    try:
        rota = db.query(Rota).filter(Rota.id == rota_id).first()
        
        if not rota:
            return None
        db.delete(rota)
        db.commit()

        return {"message": "Rota deletada com sucesso"}
    finally:
        db.close()