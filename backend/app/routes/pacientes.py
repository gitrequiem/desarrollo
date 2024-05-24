from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.localidad import Localidad
from app.models.nacionalidad import Nacionalidad
from app.models.doctipo import DocTipo
from app.models.paciente import Paciente, PacienteSchema

# Crear un blueprint para las rutas de pacientes
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
pacientes_bp = Blueprint('pacientes', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
paciente_schema = PacienteSchema()
pacientes_schema = PacienteSchema(many=True)

# Ruta para obtener todos los pacientes
@pacientes_bp.route('/pacientes', methods=['GET'])
def get_pacientes():
    session = SessionLocal()
    try:
        # Consultar todos los pacientes en la base de datos
        pacientes = session.query(Paciente).all()
        # Serializar el resultado usando el esquema de Paciente
        return jsonify({
            'status': 'success',
            'count': len(pacientes),
            'data': pacientes_schema.dump(pacientes)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un paciente por ID
@pacientes_bp.route('/pacientes/<int:id>', methods=['GET'])
def get_paciente(id):
    session = SessionLocal()
    try:
        # Consultar un paciente por ID en la base de datos
        paciente = session.query(Paciente).get(id)
        # Verificar si el paciente existe
        if not paciente:
            return jsonify({'status': 'error', 'message': 'Paciente no encontrado'}), 404
        # Serializar el resultado usando el esquema de paciente
        return jsonify({
            'status': 'success',
            'data': paciente_schema.dump(paciente)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un paciente por nombre
@pacientes_bp.route('/pacientes/<string:nombre>', methods=['GET'])
def get_paciente_by_paciente(nombre):
    session = SessionLocal()
    try:
        # Construcción de query para buscar por apellidos o nombres de paciente
        paciente = session.query(Paciente).filter(
            Paciente.apellidos.like('%' + nombre + '%') |
            Paciente.nombre.like('%' + nombre + '%')
        ).first()
        
        # Verifica si el paciente existe
        if not paciente:
            return jsonify({'status':'error', 'message': 'Paciente no existente.'})
        
        return jsonify({
            'status': 'success',
            'data': paciente_schema.dump(paciente)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un paciente número de documento
@pacientes_bp.route('/pacientes/<int:doc_numero>', methods=['GET'])
def get_paciente_by_doc_numero(doc_numero):
    session = SessionLocal()
    try:
        # Consultar un paciente por numero de documento en la base de datos
        paciente = session.query(Paciente).get(doc_numero)
        # Verificar si el paciente existe
        if not paciente:
            return jsonify({'status': 'error', 'message': 'Paciente no encontrado'}), 404
        # Serializar el resultado usando el esquema de paciente
        return jsonify({
            'status': 'success',
            'data': paciente_schema.dump(paciente)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear un nuevo paciente
@pacientes_bp.route('/pacientes', methods=['POST'])
def create_paciente():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el id_doc_tipo
        if 'id_doc_tipo' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "id_doc_tipo"'}), 400
        # Validar si se proporciona el numero de documento
        if 'doc_numero' not in data:
            return jsonify({'status':'error', 'message': 'Falta campo "doc_numero"'}), 400
        # Validar si se proporcionan los apellidos del paciente
        if 'apellidos' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "apellidos"'}), 400
        # Validar si se proporcionan el nombre del paciente
        if 'nombre' not in data:
            return jsonify({'status':'error', 'message': 'Falta campo "nombre"'}), 400
        # Validar si se proporciona el id_localidad del paciente
        if 'id_localidad' not in data:
            return jsonify({'status': 'error', 'message':'Falta campo "id_localidad"'}),400
        # Validar si se proporciona el id_nacionalidad del paciente
        if 'id_nacionalidad' not in data:
            return jsonify({'status': 'error', 'message':'Falta campo "id_nacionalidad"'}),400
        
        # Validar el largo de apellidos
        if len(data['apellidos']) < 1 or len(data['apellidos']) > 60:
            return jsonify({'status':'error', 'message': 'Los apellidos deben tener entre 1 y 60 caracteres'}), 400
        
        # Validar el largo de nombres
        if len(data['nombre']) < 1 or len(data['nombre']) > 60:
            return jsonify({'status':'error', 'message':'El nombre debe tener entre 1 y 60 caracteres'}), 400
        
        # Verificar si existe paciente por numero de documento
        paciente_existente = session.query(Paciente).filter_by(doc_numero=data['doc_numero']).first()
        if paciente_existente:
            return jsonify({'status':'error','message':'El paciente ya existe'}),400

        # Verificar si el id_doc_tipo existe en la tabla doc_tipos
        doc_tipo_existente = session.query(DocTipo).get(data['id_doc_tipo'])
        if not doc_tipo_existente:
            return jsonify({'status':'error', 'message': 'El tipo de documento no existe'}), 400
        
        # Verificar si el id_localidad existe en la tabla localidades
        localidad_existente = session.query(Localidad).get(data['id_localidad'])
        if not localidad_existente:
            return jsonify({'status':'error', 'message': 'La localidad no existe'}), 400
        
         # Verificar si el id_nacionalidad existe en la tabla nacionalidades
        nacionalidad_existente = session.query(Nacionalidad).get(data['id_nacionalidad'])
        if not nacionalidad_existente:
            return jsonify({'status':'error', 'message': 'La nacionalidad no existe'}), 400
        
        # Crear una nueva instancia de paciente
        nuevo_paciente = Paciente(id_doc_tipo=data['id_doc_tipo'], 
                                  doc_numero=data['doc_numero'], 
                                  apellidos=data['apellidos'], nombre=data['nombre'], 
                                  id_localidad=data['id_localidad'], 
                                  id_nacionalidad=data['id_nacionalidad'])
        
        # Agregar el nuevo paciente a la sesión y confirmar la transacción
        session.add(nuevo_paciente)
        session.commit()
        
        # Serializar el resultado usando el esquema de paciente
        return jsonify({
            'status': 'success',
            'message': 'Paciente creado correctamente',
            'data': paciente_schema.dump(nuevo_paciente)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar un paciente por ID
@pacientes_bp.route('/pacientes/<int:id>', methods=['PUT'])
def update_paciente(id):
    session = SessionLocal()
    try:
        # Recupera paciente por el ID
        paciente = session.query(Paciente).filter_by(id_paciente=id).first()
        if not paciente:
            return jsonify({'status':'error', 'message':'Paciente no encontrado'}), 400
        
        data = request.json
        # Validar si se proporcionan los apellidos del paciente
        if 'apellidos' not in data or 'nombre' not in data:
            return jsonify({'status':'error', 'message':'No se encuentra ese apellido y/o nombre'}), 400
        
        # Validar si apellidos y nombres son únicos
        nuevo_paciente_nombre = data['apellidos'] + ' ' + data['nombre']
        paciente_existente = session.query(Paciente).filter(
            Paciente.doc_numero == data['doc_numero'],
            Paciente.apellidos == data['apellidos'],
            Paciente.nombre == data['nombre'],
            Paciente.id_paciente != id 
        ).one_or_none()
        if paciente_existente:
            return jsonify({'status':'error', 'message':'Ya existe un paciente con ese nombre y apellido'}), 400
        
        # Valida si esta el id_doc_tipo en la tabla doc_tipos
        if 'id_doc_tipo' in data:
            doc_tipo = session.query(DocTipo).filter_by(id_doc_tipo=data['id_doc_tipo']).first()
            if not doc_tipo:
                return jsonify({'status':'error', 'message':'id_doc_tipo Inválido'}), 400
            paciente.id_doc_tipo = data['id_doc_tipo']

        # Valida si esta el id_localidad en a tabla localidades
        if 'id_localidad' in data:
            localidad = session.query(Localidad).filter_by(id_localidad=data['id_localidad']).first()
            if not localidad:
                return jsonify({'status':'error', 'message':'id_localidad Inválido'}), 400
            paciente.id_localidad = data['id_localidad']
        
        # Valida si esta el id_nacionalidad en la tabla nacionalidades
        if 'id_nacionalidad' in data:
            nacionalidad = session.query(Nacionalidad).filter_by(id_nacionalidad=data['id_nacionalidad']).first()
            if not nacionalidad:
                return jsonify({'status':'error', 'message':'id_nacionalidad Inválido'}), 400
        
        # Modifica los datos del paciente seleccionado
        paciente.apellidos = data['apellidos']
        paciente.nombre = data['nombre']
        paciente.doc_numero = data['doc_numero']
        if 'id_doc_tipo' in data:
            paciente.id_doc_tipo = data['id_doc_tipo']
        if 'id_localidad' in data:
            paciente.id_localidad = data['id_localidad']
        if 'id_nacionalidad' in data:
            paciente.id_nacionalidad = data ['id_nacionalidad']
        
        # Confirmar la transacción
        session.commit()
         # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'message': 'Paciente actualizado correctamente',
            'data': paciente_schema.dump(paciente)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un paciente por ID
@pacientes_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def delete_paciente(id):
    session = SessionLocal()
    try:
        # Consultar paciente por id en la base de datos
        paciente = session.query(Paciente).get(id)
        # Verificar si el paciente existe
        if not paciente:
            return jsonify({'status': 'error', 'message': 'Paciente no encontrado'}), 404
        # Eliminar el paciente de la base de datos
        session.delete(paciente)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Paciente eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un paciente por numero de documento
@pacientes_bp.route('/pacientes/<int:doc_numero>', methods=['DELETE'])
def delete_paciente_by_doc_numero(doc_numero):
    session = SessionLocal()
    try:
        # Consultar paciente por id en la base de datos
        paciente = session.query(Paciente).filter_by(doc_numero=doc_numero).first()
        # Verificar si el paciente existe
        if not paciente:
            return jsonify({'status': 'error', 'message': 'Paciente no encontrado'}), 404
        # Eliminar el paciente de la base de datos
        session.delete(paciente)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Paciente eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
    
    