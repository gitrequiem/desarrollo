from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class StaffTipo(Base):
    __tablename__ = 'staff_tipos'
    id_staff_tipo = Column(Integer, primary_key=True, autoincrement=True)
    staff_tipo = Column(String(50),unique=True, nullable=False)

    def __init__(self, staff_tipo):
        self.staff_tipo = staff_tipo
    
    def __repr__(self):
        return '<staff_tipo {}>'.format(self.staff_tipo)
    
    def serializable(self):
        return{
            'id_staff_tipo': self.id_staff_tipo,
            'staff_tipo' : self.staff_tipo
        }

# Esquema de validación para StaffTipo utilizando Marshmallow
class StaffTipoSchema(Schema):
    """
    Esquema de validación para la entidad StaffTipo.
    """
    id_staff_tipo = fields.Int(dump_only=True)
    staff_tipo = fields.Str(required=True, validate=validate.Length(min=1, max=50))