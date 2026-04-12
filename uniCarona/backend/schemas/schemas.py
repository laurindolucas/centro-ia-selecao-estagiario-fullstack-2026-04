from pydantic import BaseModel

class UserCreate(BaseModel):
    nome: str
    descricao: str
    email: str
    
class RideCreate(BaseModel):
    usuario_id: int
    origem: str
    destino: str
    horario: str