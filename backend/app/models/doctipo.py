from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String
from app.configs.database import Base

class DocTipo(Base):
    __tablename__ = 'doc_tipos'
    id_doc_tipo = Column(Integer, primary_key= True, autoincrement=True)
    doc_tipo = Column(String(50),unique=True, nullable=False)
    
    def __init__(self, doc_tipo):
        self.doc_tipo = doc_tipo
    
    def __repr__(self):
        return '<doc_tipo {}>'.format(self.doc_tipo)
    
    def serializable(self):
        return{
            'id_doc_tipo': self.id_doc_tipo,
            'doc_tipo' : self.doc_tipo
        }

# Esquema de validación para DocTipo utilizando Marshmallow
class DocTipoSchema(Schema):
    """
    Esquema de validación para la entidad DocTipo.
    """
    id_doc_tipo = fields.Int(dump_only=True)
    doc_tipo = fields.Str(required=True, validate=validate.Length(min=1, max=50))