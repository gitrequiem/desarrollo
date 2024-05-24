from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class StaffRolCirugia(Base):
    __tablename__ = 'staff_roles_cirugia'
    id_staff_rol_cirugia = Column(Integer, primary_key=True, autoincrement=True)
    rol_cirugia = Column(String(50), unique=True, nullable=False)
    
    def __init__(self, rol_cirugia):
        self.rol_cirugia = rol_cirugia
    
    def __repr__(self):
        return'<rol_cirugia {}>'.format(self.rol_cirugia)
    
    def serializable(self):
        return{
            'id_staff_rol_cirugia' : self.id_staff_rol_cirugia,
            'rol_cirugia' : self.rol_cirugia
            
        }
    
# Esquema de validación para StaffRolCirugia utilizando Marshmallow
class StaffRolCirugiaSchema(Schema):
    """
    Esquema de validación para la entidad StaffRolCirugia.
    """
    id_staff_rol_cirugia = fields.Int(dump_only=True)
    rol_cirugia = fields.Str(required=True, validate=validate.Length(min=1, max=50))