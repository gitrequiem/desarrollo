from marshmallow import Schema, fields, validate
from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship

class Paciente(Base):
    __tablename__ = 'pacientes'
    id_paciente = Column(Integer, primary_key=True, autoincrement=True)
    id_doc_tipo = Column(Integer, ForeignKey('doc_tipos.id_doc_tipo', ondelete='CASCADE'), nullable=False)
    doc_numero = Column(Integer, nullable=False)
    apellidos = Column(String(50), unique=True, nullable=False)
    nombre = Column(String(50), unique=True, nullable=False)
    id_localidad = Column(Integer, ForeignKey('localidades.id_localidad', ondelete='CASCADE'), nullable=False)
    id_nacionalidad = Column(Integer, ForeignKey('nacionalidades.id_nacionalidad', ondelete='CASCADE'), nullable=False)
    
    doc_tipo = relationship('DocTipo', backref='pacientes')
    localidad = relationship('Localidad', backref='pacientes')
    nacionalidad = relationship('Nacionalidad', backref='pacientes')
    
    def __init__(self,id_doc_tipo, doc_numero, apellidos, nombre, id_localidad, id_nacionalidad):
        self.id_doc_tipo = id_doc_tipo
        self.doc_numero = doc_numero
        self.apellidos = apellidos
        self.nombre = nombre
        self.id_localidad = id_localidad
        self.id_nacionalidad = id_nacionalidad

    def __repr__(self):
        return'<doc_numero {}>'.format(self.doc_numero), '<apellidos {}>'.format(self.apellidos), '<nombre {}>'.format(self.nombre)
    
    def serializable(self):
        return{
            'id_paciente' : self.id_paciente,
            'doc_numero' : self.doc_numero,
            'apellidos' : self.apellidos,
            'nombre' : self.nombre
        }

# Esquema de validación para Paciente utilizando Marshmallow
class PacienteSchema(Schema):
    """
    Esquema de validación para la entidad Paciente.
    """
    id_paciente = fields.Int(dump_only=True)
    id_doc_tipo = fields.Int(required= True)
    doc_numero = fields.Int(dump_only=True)
    apellidos = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    id_localidad = fields.Int(required= True)
    id_nacionalidad = fields.Int(required= True)