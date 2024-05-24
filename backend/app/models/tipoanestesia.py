from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class TipoAnestesia(Base):
    __tablename__ = 'tipos_anestesia'
    id_tipo_anestesia = Column(Integer, primary_key=True, autoincrement=True)
    tipo_anestesia = Column(String(50),unique=True, nullable=False)
    
    def __init__(self, tipo_anestesia):
        self.tipo_anestesia = tipo_anestesia
        
    def __repr__(self):
        return '<tipo_anestesia {}>'.format(self.tipo_anestesia)
    
    def serializable(self):
        return{
            'id_tipo_anestesia' : self.id_tipo_anestesia,
            'tipo_anestesia' : self.tipo_anestesia
        }

# Esquema de validación para TipoAnestesia utilizando Marshmallow
class TipoAnestesiaSchema(Schema):
    """
    Esquema de validación para la entidad TipoAnestesia.
    """
    id_tipo_anestesia = fields.Int(dump_only=True)
    tipo_anestesia = fields.Str(required=True, validate=validate.Length(min=1, max=50))