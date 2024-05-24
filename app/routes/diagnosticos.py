from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.diagnostico import Diagnostico, DiagnosticoSchema
from app.models.especialidad import Especialidad

# Crear un blueprint para las rutas de diagnosticos
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
diagnosticos_bp = Blueprint('diagnosticos', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
diagnostico_schema = DiagnosticoSchema()
diagnosticos_schema = DiagnosticoSchema(many=True)

# Ruta para obtener todos los diagnosticos
@diagnosticos_bp.route('/diagnosticos', methods=['GET'])
def get_diagnosticos():
    session = SessionLocal()
    try:
        # Consultar todos los diagnosticos en la base de datos
        diagnosticos = session.query(Diagnostico).all()
        # Serializar el resultado usando el esquema de Diagnostico
        return jsonify({
            'status': 'success',
            'count': len(diagnosticos),
            'data': diagnosticos_schema.dump(diagnosticos)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un diagnostico por ID
@diagnosticos_bp.route('/diagnosticos/<int:id>', methods=['GET'])
def get_diagnostico(id):
    session = SessionLocal()
    try:
        # Consultar el diagnostico por ID en la base de datos
        diagnostico = session.query(Diagnostico).get(id)
        # Verificar si el diagnostico existe
        if not diagnostico:
            return jsonify({'status': 'error', 'message': 'Diagnóstico no encontrado'}), 404
        # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'data': diagnostico_schema.dump(diagnostico)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un diagnostico por nombre
@diagnosticos_bp.route('/diagnosticos/<string:nombre>', methods=['GET'])
def get_diagnostico_by_diagnostico(nombre):
    session = SessionLocal()
    try:
        # Consultar el diagnostico por nombre en la base de datos
        diagnostico = session.query(Diagnostico).filter_by(diagnostico=nombre).first()
        # Verificar si el diagnostico existe
        if not diagnostico:
            return jsonify({'status': 'error', 'message': 'Diagnóstico no encontrado'}), 404
        # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'data': diagnostico_schema.dump(diagnostico)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear un nuevo diagnostico
@diagnosticos_bp.route('/diagnosticos', methods=['POST'])
def create_diagnostico():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del diagnostico
        if 'diagnostico' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "diagnostico"'}), 400
        
        # Verificar si el diagnostico ya existe en la base de datos
        diagnostico_existente = session.query(Diagnostico).filter_by(diagnostico=data['diagnostico']).first()
        if diagnostico_existente:
            return jsonify({'status': 'error', 'message': 'El diagnóstico ya existe'}), 400
        
        
        # Validar si se proporcion el id_especialidad
        if 'id_especialidad' not in data:
            return jsonify({'status':'error', 'message': 'Falta campo "id_especialidad"'}),400
        
        # Verificar si el id_especialidad existe en la tabla especialidades
        especialidad_existente = session.query(Especialidad).get(data['id_especialidad'])
        if not especialidad_existente:
            return jsonify({'status':'error', 'message': 'La especialidad no existe'}), 400
        
        # Crear una nueva instancia de Diagnostico
        nuevo_diagnostico = Diagnostico(diagnostico=data['diagnostico'], id_especialidad=data['id_especialidad'])
        
        # Agregar el nuevo diagnostico a la sesión y confirmar la transacción
        session.add(nuevo_diagnostico)
        session.commit()
        
        # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'message': 'Tipo de documento creado correctamente',
            'data': diagnostico_schema.dump(nuevo_diagnostico)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
        
# Ruta para actualizar un diagnostico por ID
@diagnosticos_bp.route('/diagnosticos/<int:id>', methods=['PUT'])
def update_diagnostico(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del diagnostico
        if 'diagnostico' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "diagnostico"'}), 400
        
        # Consultar el diagnostico por ID en la base de datos
        diagnostico = session.query(Diagnostico).get(id)
        
        # Verificar si el diagnostico existe
        if not diagnostico:
            return jsonify({'status': 'error', 'message': 'Diagnóstico no encontrado'}), 404
        
        # Verificar si el nuevo diagnostico ya existe en la base de datos
        nuevo_diagnostico_existente = session.query(Diagnostico).filter_by(diagnostico=data['diagnostico']).first()
        if nuevo_diagnostico_existente:
            return jsonify({'status': 'error', 'message': 'El diagnóstico ya existe'}), 400
        
        # Actualizar el nombre del diagnostico
        diagnostico.diagnostico = data['diagnostico']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'message': 'Diagnóstico actualizado correctamente',
            'data': diagnostico_schema.dump(diagnostico)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un diagnostico por ID
@diagnosticos_bp.route('/diagnosticos/<int:id>', methods=['DELETE'])
def delete_diagnostico(id):
    session = SessionLocal()
    try:
        # Consultar el diagnostico por ID en la base de datos
        diagnostico = session.query(Diagnostico).get(id)
        # Verificar si el diagnostico existe
        if not diagnostico:
            return jsonify({'status': 'error', 'message': 'Diagnóstico no encontrado'}), 404
        # Eliminar el diagnostico de la base de datos
        session.delete(diagnostico)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Diagnóstico eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
