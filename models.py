from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


Base  = declarative_base()

class Kit(Base):
    __tablename__ = 'Kit'
    id  = Column(Integer, primary_key=True, index=True)
    nome_instrumento = Column(String)

class Cirurgia(Base):
    __tablename__ = 'Cirurgia'
    id = Column(Integer, primary_key=True, index=True)
    CRM_Medico = Column(Integer)
    CPF_Paciente = Column(Integer)
    Sala_Hospital = Column(Integer)
    Tipo_Cirurgia = Column(String)
    Kit_id = Column(Integer, ForeignKey('Kit.id'))
    
    
