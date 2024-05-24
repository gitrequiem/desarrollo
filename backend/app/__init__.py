from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración desde config.py
# app.config.from_object('app.configs.config.Config')

# Inicializar la base de datos
# from app.configs.database import init_db
# init_db(app)

# Registrar rutas Blueprint
# app.register_blueprint(nacionalidades.nacionalidades_bp)
# app.register_blueprint(index.index_bp)

# Importar rutas
from app.routes import nacionalidades, index, provincias, doctipos, especialidades, intervenciones, stafftipos, staffrolescirugia, tiposanestesia, diagnosticos, localidades, staffs, pacientes

#######################
def init_app():
    # configuracion de la app
    app.debug = True

    # Configuración SQLALchemy desde config.py
    app.config.from_object('app.configs.config.Config')
    
    # Inicializar la base de datos
    from app.configs.database import init_db
    init_db(app)

    # Registrar rutas Blueprint
    app.register_blueprint(pacientes.pacientes_bp)
    app.register_blueprint(staffs.staffs_bp)
    app.register_blueprint(localidades.localidades_bp)
    app.register_blueprint(diagnosticos.diagnosticos_bp)
    app.register_blueprint(tiposanestesia.tiposanestesia_bp)
    app.register_blueprint(staffrolescirugia.staffrolescirugia_bp)
    app.register_blueprint(stafftipos.stafftipos_bp)
    app.register_blueprint(intervenciones.intervenciones_bp)
    app.register_blueprint(especialidades.especialidades_bp)
    app.register_blueprint(doctipos.doctipos_bp)
    app.register_blueprint(provincias.provincias_bp)
    app.register_blueprint(nacionalidades.nacionalidades_bp)
    app.register_blueprint(index.index_bp)
    
    return app