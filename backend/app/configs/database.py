from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from app.configs.config import Config

# Crear motor de base de datos
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

# Crear una base declarativa
Base = declarative_base()

# Crear una sesión configurada
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db(app):
    # Importar modelos aquí para asegurarse de que estén registrados en la base de datos
    from app.models.nacionalidad import Nacionalidad
    from app.models.provincia import Provincia
    from app.models.localidad import Localidad
    from app.models.doctipo import DocTipo
    from app.models.unidad import Unidad
    from app.models.stafftipo import StaffTipo
    from app.models.especialidad import Especialidad
    from app.models.intervencion import Intervencion
    from app.models.tipoanestesia import TipoAnestesia
    from app.models.diagnostico import Diagnostico
    from app.models.staff import Staff
    from app.models.staffrolcirugia import StaffRolCirugia
    from app.models.paciente import Paciente
    Base.metadata.create_all(bind=engine)
