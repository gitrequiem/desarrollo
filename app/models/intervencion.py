from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class Intervencion(Base):
    __tablename__ = 'intervenciones'
    id_intervencion = Column(Integer, primary_key=True, autoincrement=True)
    intervencion = Column(String(60),unique=True, nullable=False)
    
    def __init__(self, intervencion):
        self.intervencion = intervencion
    
    def __repr__(self):
        return '<intervencion {}>'.format(self.intervencion)
    
    def serializable(self):
        return{
            'id_intervencion' : self.id_intervencion,
            'intervencion' : self.intervencion
        }

# Esquema de validación para Intervencion utilizando Marshmallow
class IntervencionSchema(Schema):
    """
    Esquema de validación para la entidad Intervencion.
    """
    id_intervencion = fields.Int(dump_only=True)
    intervencion = fields.Str(required=True, validate=validate.Length(min=1, max=60))