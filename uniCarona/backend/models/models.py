from sqlalchemy import (Column, Integer, String, ForeignKey)
from database.connection import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(String(120), nullable=False)
    descricao = Column(String(250))
    email = Column(String(120), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    
    
class Rota(Base):
    __tablename__ = "rotas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    origem = Column(String(120), nullable=False)
    destino = Column(String(120), nullable=False)
    horario = Column(String(20), nullable=False)