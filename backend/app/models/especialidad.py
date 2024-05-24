from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class Especialidad(Base):
    __tablename__ = 'especialidades'
    id_especialidad = Column(Integer, primary_key=True, autoincrement=True)
    especialidad = Column(String(50),unique=True, nullable=False)
    
    def __init__(self, especialidad):
        self.especialidad = especialidad
    
    def __repr__(self):
        return '<especialidad {}>'.format(self.especialidad)
    
    def serializable(self):
        return{
            'id_especialidad' : self.id_especialidad,
            'especialidad' : self.especialidad
        }

# Esquema de validación para Especialidad utilizando Marshmallow
class EspecialidadSchema(Schema):
    """
    Esquema de validación para la entidad Especialidad.
    """
    id_especialidad = fields.Int(dump_only=True)
    especialidad = fields.Str(required=True, validate=validate.Length(min=1, max=50))