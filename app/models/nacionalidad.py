from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class Nacionalidad(Base):
    __tablename__ = 'nacionalidades'
    
    id_nacionalidad = Column(Integer, primary_key=True, autoincrement=True)
    nacionalidad = Column(String(50), unique=True, nullable=False)

    def __init__(self, nacionalidad):
        self.nacionalidad = nacionalidad

    def __repr__(self):
        return '<Nacionalidad {}>'.format(self.nacionalidad)

    def serialize(self):
        """
        Método para serializar los atributos de la instancia.
        """
        return {
            'id_nacionalidad': self.id_nacionalidad,
            'nacionalidad': self.nacionalidad
        }
    
# Esquema de validación para Nacionalidad utilizando Marshmallow
class NacionalidadSchema(Schema):
    """
    Esquema de validación para la entidad Nacionalidad.
    """
    id_nacionalidad = fields.Int(dump_only=True)
    nacionalidad = fields.Str(required=True, validate=validate.Length(min=1, max=50))
