from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship

class Staff(Base):
    __tablename__ = 'staff'
    id_staff = Column(Integer, primary_key=True, autoincrement=True)
    apellidos = Column(String(60), unique=True, nullable=False)
    nombres = Column(String(60), unique= True, nullable=False)
    id_staff_tipo = Column(Integer, ForeignKey('staff_tipos.id_staff_tipo', ondelete='CASCADE'), nullable=False)
    
    staff_tipo = relationship('StaffTipo', backref='staff')
    
    def __init__(self, apellidos, nombres, id_staff_tipo):
        self.apellidos = apellidos
        self.nombres = nombres
        self.id_staff_tipo = id_staff_tipo
    
    def __repr__(self):
        return '<apellidos {}>'.format(self.apellidos), '<nombres {}>'.format(self.apellidos)
    
    def serializable(self):
        return{
            'id_staff' : self.id_staff,
            'apellidos' : self.apellidos,
            'nombres' : self.nombres
        }

# Esquema de validación para Staff utilizando Marshmallow
class StaffSchema(Schema):
    """
    Esquema de validación para la entidad Staff.
    """
    id_staff = fields.Int(dump_only=True)
    apellidos = fields.Str(required=True, validate=validate.Length(min=1, max=60))
    nombres = fields.Str(required=True, validate=validate.Length(min=1, max=60))
    id_staff_tipo = fields.Int(required=True)