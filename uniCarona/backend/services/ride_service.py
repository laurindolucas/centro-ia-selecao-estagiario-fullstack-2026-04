from database.connection import SessionLocal
from models.models import Rota
from services.location_service import obter_coordenadas

def criar_rota(data):
    db = SessionLocal()
    
    try:
        lat_o, lon_o = obter_coordenadas(data.origem)
        lat_d, lon_d = obter_coordenadas(data.destino)

        if lat_o is None or lat_d is None:
            return {"error": "Endereço inválido"}
        rota = Rota(
           usuario_id=data.usuario_id,
           origem = data.origem,
           destino = data.destino,
           horario = data.horario,
           lat_origem=lat_o,
           lon_origem=lon_o,
           lat_destino=lat_d,
           lon_destino=lon_d
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
        lat_o, lon_o = obter_coordenadas(data.origem)
        lat_d, lon_d = obter_coordenadas(data.destino)

        if not rota:
            return {"message": "Rota não encontrada!"}
        
        rota.origem = data.origem
        rota.destino = data.destino
        rota.horario = data.horario
        rota.lat_origem = lat_o
        rota.lon_origem = lon_o
        rota.lat_destino = lat_d
        rota.lon_destino = lon_d
        
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