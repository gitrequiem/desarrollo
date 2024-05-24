from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class Provincia(Base):
    __tablename__ = 'provincias'
    id_provincia = Column(Integer, primary_key=True, autoincrement=True)
    provincia = Column(String(50),unique=True, nullable=False)
    
    def __init__ (self, provincia):
        self.provincia = provincia
    
    def __repr__(self):
        return '<provincia {}>'.format(self.provincia)
    
    def serializable(self):
        return{
            'id_provincia': self.id_provincia,
            'provincia': self.provincia
        }

# Esquema de validación para Provincia utilizando Marshmallow
class ProvinciaSchema(Schema):
    """
    Esquema de validación para la entidad Provincia.
    """
    id_provincia = fields.Int(dump_only=True)
    provincia = fields.Str(required=True, validate=validate.Length(min=1, max=50))