from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.intervencion import Intervencion, IntervencionSchema

# Crear un blueprint para las rutas de intervenciones
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
intervenciones_bp = Blueprint('intervenciones', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
intervencion_schema = IntervencionSchema()
intervenciones_schema = IntervencionSchema(many=True)

# Ruta para obtener todas las intervenciones
@intervenciones_bp.route('/intervenciones', methods=['GET'])
def get_intervenciones():
    session = SessionLocal()
    try:
        # Consultar todas las intervenciones en la base de datos
        intervenciones = session.query(Intervencion).all()
        # Serializar el resultado usando el esquema de Intervencion
        return jsonify({
            'status': 'success',
            'count': len(intervenciones),
            'data': intervenciones_schema.dump(intervenciones)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener una intervencion por ID
@intervenciones_bp.route('/intervenciones/<int:id>', methods=['GET'])
def get_intervencion(id):
    session = SessionLocal()
    try:
        # Consultar un intervencion por ID en la base de datos
        intervencion = session.query(Intervencion).get(id)
        # Verificar si la intervencion existe
        if not intervencion:
            return jsonify({'status': 'error', 'message': 'Intervención no encontrada'}), 404
        # Serializar el resultado usando el esquema de intervencion
        return jsonify({
            'status': 'success',
            'data': intervencion_schema.dump(intervencion)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una intervencion por nombre
@intervenciones_bp.route('/intervenciones/<string:nombre>', methods=['GET'])
def get_intervencion_by_intervencion(nombre):
    session = SessionLocal()
    try:
        # Consultar la intervencion por nombre en la base de datos
        intervencion = session.query(Intervencion).filter_by(intervencion=nombre).first()
        # Verificar si la intervencion existe
        if not intervencion:
            return jsonify({'status': 'error', 'message': 'Intervención no encontrada'}), 404
        # Serializar el resultado usando el esquema de intervencion
        return jsonify({
            'status': 'success',
            'data': intervencion_schema.dump(intervencion)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear una nueva intervencion
@intervenciones_bp.route('/intervenciones', methods=['POST'])
def create_intervencion():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la intervencion
        if 'intervencion' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "intervencion"'}), 400
        
        # Verificar si la intervencion ya existe en la base de datos
        intervencion_existente = session.query(Intervencion).filter_by(intervencion=data['intervencion']).first()
        if intervencion_existente:
            return jsonify({'status': 'error', 'message': 'la intervención ya existe'}), 400
        
        # Crear una nueva instancia de Intervencion
        nueva_intervencion = Intervencion(intervencion=data['intervencion'])
        
        # Agregar la nueva intervencion a la sesión y confirmar la transacción
        session.add(nueva_intervencion)
        session.commit()
        
        # Serializar el resultado usando el esquema de intervencion
        return jsonify({
            'status': 'success',
            'message': 'Intervención creada correctamente',
            'data': intervencion_schema.dump(nueva_intervencion)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar una intervencion por ID
@intervenciones_bp.route('/intervenciones/<int:id>', methods=['PUT'])
def update_intervencion(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la intervencion
        if 'intervencion' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "intervencion"'}), 400
        
        # Consultar la intervencion por ID en la base de datos
        intervencion = session.query(Intervencion).get(id)
        
        # Verificar si la intervencion existe
        if not intervencion:
            return jsonify({'status': 'error', 'message': 'Intervención no encontrada'}), 404
        
        # Verificar si la nueva intervencion ya existe en la base de datos
        nueva_intervencion_existente = session.query(Intervencion).filter_by(intervencion=data['intervencion']).first()
        if nueva_intervencion_existente:
            return jsonify({'status': 'error', 'message': 'La intervención ya existe'}), 400
        
        # Actualizar el nombre de la intervencion
        intervencion.intervencion = data['intervencion']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de intervencion
        return jsonify({
            'status': 'success',
            'message': 'Intervención actualizada correctamente',
            'data': intervencion_schema.dump(intervencion)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar una intervencion por ID
@intervenciones_bp.route('/intervenciones/<int:id>', methods=['DELETE'])
def delete_intervencion(id):
    session = SessionLocal()
    try:
        # Consultar la intervencion por ID en la base de datos
        intervencion = session.query(Intervencion).get(id)
        # Verificar si la intervencion existe
        if not intervencion:
            return jsonify({'status': 'error', 'message': 'Intervención no encontrada'}), 404
        # Eliminar la intervención de la base de datos
        session.delete(intervencion)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Intervención eliminada correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()