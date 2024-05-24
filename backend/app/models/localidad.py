from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship

class Localidad(Base):
    __tablename__ = 'localidades'
    id_localidad = Column(Integer, primary_key=True, autoincrement=True)
    localidad = Column(String(60),unique=True, nullable=False)
    id_provincia = Column(Integer, ForeignKey('provincias.id_provincia',ondelete='CASCADE'), nullable=False)
    
    provincia = relationship('Provincia', backref='localidades')
    
    def __init__(self, localidad, id_provincia):
        self.localidad = localidad
        self.id_provincia = id_provincia
        
    def __repr__(self):
        return '<localidad {}>'.format(self.localidad)
    
    def serializable(self):
        return{
            'id_localidad' : self.id_localidad,
            'localidad' : self.localidad
        }

# Esquema de validación para Localidad utilizando Marshmallow
class LocalidadSchema(Schema):
    """
    Esquema de validación para la entidad Localidad.
    """
    id_localidad = fields.Int(dump_only=True)
    localidad = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    id_provincia = fields.Int(required=True)