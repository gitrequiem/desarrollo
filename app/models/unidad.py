from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class Unidad(Base):
    __tablename__ = 'unidades'
    id_unidad = Column(Integer, primary_key=True, autoincrement=True)
    unidad = Column(String(50),unique=True, nullable=False)
    
    def __init__(self, unidad):
        self.unidad = unidad
    
    def __repr__(self):
        return '<unidad {}>'.format(self.unidad)
    
    def serializable(self):
        return{
            'id_unidad' : self.id_unidad,
            'unidad' : self.unidad
        }

# Esquema de validación para Unidad utilizando Marshmallow
class UnidadSchema(Schema):
    """
    Esquema de validación para la entidad Unidad.
    """
    id_unidad = fields.Int(dump_only=True)
    unidad = fields.Str(required=True, validate=validate.Length(min=1, max=50))