from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.especialidad import Especialidad, EspecialidadSchema

# Crear un blueprint para las rutas de especialidades
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
especialidades_bp = Blueprint('especialidades', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
especialidad_schema = EspecialidadSchema()
especialidades_schema = EspecialidadSchema(many=True)

# Ruta para obtener todas las especialidades
@especialidades_bp.route('/especialidades', methods=['GET'])
def get_especialidades():
    session = SessionLocal()
    try:
        # Consultar todas las especialidades en la base de datos
        especialidades = session.query(Especialidad).all()
        # Serializar el resultado usando el esquema de Especialidad
        return jsonify({
            'status': 'success',
            'count': len(especialidades),
            'data': especialidades_schema.dump(especialidades)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener una especialidad por ID
@especialidades_bp.route('/especialidades/<int:id>', methods=['GET'])
def get_especialidad(id):
    session = SessionLocal()
    try:
        # Consultar la especialidad por ID en la base de datos
        especialidad = session.query(Especialidad).get(id)
        # Verificar si la especialidad existe
        if not especialidad:
            return jsonify({'status': 'error', 'message': 'Especialidad no encontrada'}), 404
        # Serializar el resultado usando el esquema de especialidad
        return jsonify({
            'status': 'success',
            'data': especialidad_schema.dump(especialidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una especialidad por nombre
@especialidades_bp.route('/especialidades/<string:nombre>', methods=['GET'])
def get_especialidad_by_especialidad(nombre):
    session = SessionLocal()
    try:
        # Consultar la especialidad por nombre en la base de datos
        especialidad = session.query(Especialidad).filter_by(especialidad=nombre).first()
        # Verificar si la especialidad existe
        if not especialidad:
            return jsonify({'status': 'error', 'message': 'Especialidad no encontrada'}), 404
        # Serializar el resultado usando el esquema de especialidad
        return jsonify({
            'status': 'success',
            'data': especialidad_schema.dump(especialidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear una nueva especialidad
@especialidades_bp.route('/especialidades', methods=['POST'])
def create_especialidad():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la especialidad
        if 'especialidad' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "especialidad"'}), 400
        
        # Verificar si la especialidad ya existe en la base de datos
        especialidad_existente = session.query(Especialidad).filter_by(especialidad=data['especialidad']).first()
        if especialidad_existente:
            return jsonify({'status': 'error', 'message': 'La especialidad ya existe'}), 400
        
        # Crear una nueva instancia de Especialidad
        nueva_especialidad = Especialidad(especialidad=data['especialidad'])
        
        # Agregar la nueva especialidad a la sesión y confirmar la transacción
        session.add(nueva_especialidad)
        session.commit()
        
        # Serializar el resultado usando el esquema de especialidad
        return jsonify({
            'status': 'success',
            'message': 'Especialidad creada correctamente',
            'data': especialidad_schema.dump(nueva_especialidad)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
        
# Ruta para actualizar una especialidad por ID
@especialidades_bp.route('/especialidades/<int:id>', methods=['PUT'])
def update_especialidad(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la especialidad
        if 'especialidad' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "especialidad"'}), 400
        
        # Consultar la especialidad por ID en la base de datos
        especialidad = session.query(Especialidad).get(id)
        
        # Verificar si la especialidad existe
        if not especialidad:
            return jsonify({'status': 'error', 'message': 'Especialidad no encontrada'}), 404
        
        # Verificar si la nueva especialidad ya existe en la base de datos
        nueva_especialidad_existente = session.query(Especialidad).filter_by(especialidad=data['especialidad']).first()
        if nueva_especialidad_existente:
            return jsonify({'status': 'error', 'message': 'La especialidad ya existe'}), 400
        
        # Actualizar el nombre de la especialidad
        especialidad.especialidad = data['especialidad']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de especialidad
        return jsonify({
            'status': 'success',
            'message': 'Especialidad actualizada correctamente',
            'data': especialidad_schema.dump(especialidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar una especialidad por ID
@especialidades_bp.route('/especialidades/<int:id>', methods=['DELETE'])
def delete_especialidad(id):
    session = SessionLocal()
    try:
        # Consultar la especialidad por ID en la base de datos
        especialidad = session.query(Especialidad).get(id)
        # Verificar si la especialidad existe
        if not especialidad:
            return jsonify({'status': 'error', 'message': 'Especialidad no encontrada'}), 404
        # Eliminar la especialidad de la base de datos
        session.delete(especialidad)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Especialidad eliminada correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()