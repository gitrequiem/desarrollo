from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship

class Diagnostico(Base):
    __tablename__ = 'diagnosticos'
    id_diagnostico = Column(Integer, primary_key=True, autoincrement=True)
    diagnostico = Column(String(60),unique=True, nullable=False)
    id_especialidad = Column(Integer, ForeignKey('especialidades.id_especialidad', ondelete='CASCADE'), nullable=False)
    
    especialidad = relationship('Especialidad', backref='diagnosticos')
    
    def __init__(self, diagnostico, id_especialidad):
        self.diagnostico = diagnostico
        self.id_especialidad = id_especialidad
    
    def __repr__(self):
        return '<diagnostico {}>'.format(self.diagnostico)
    
    def serializable (self):
        return{
            'id_diagnostico' : self.id_diagnostico,
            'diagnostico' : self.diagnostico
        }

# Esquema de validación para Diagnostico utilizando Marshmallow
class DiagnosticoSchema(Schema):
    """
    Esquema de validación para la entidad Diagnostico.
    """
    id_diagnostico = fields.Int(dump_only=True)
    diagnostico = fields.Str(required=True, validate=validate.Length(min=1, max=60))
    id_especialidad = fields.Int(required=True)