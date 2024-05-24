from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.tipoanestesia import TipoAnestesia, TipoAnestesiaSchema

# Crear un blueprint para las rutas de tiposanestesia
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
tiposanestesia_bp = Blueprint('tipos_anestesia', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
tipo_anestesia_schema = TipoAnestesiaSchema()
tipos_anestesia_schema = TipoAnestesiaSchema(many=True)

# Ruta para obtener todos los tipos de anestesia
@tiposanestesia_bp.route('/tipos_anestesia', methods=['GET'])
def get_tipos_anestesia():
    session = SessionLocal()
    try:
        # Consultar todos los tipos de anestesia en la base de datos
        tipos_anestesia = session.query(TipoAnestesia).all()
        # Serializar el resultado usando el esquema de TipoAnestesia
        return jsonify({
            'status': 'success',
            'count': len(tipos_anestesia),
            'data': tipos_anestesia_schema.dump(tipos_anestesia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un tipo de anestesia por ID
@tiposanestesia_bp.route('/tipos_anestesia/<int:id>', methods=['GET'])
def get_tipo_anestesia(id):
    session = SessionLocal()
    try:
        # Consultar el tipo de anestesia por ID en la base de datos
        tipo_anestesia = session.query(TipoAnestesia).get(id)
        # Verificar si el tipo de anestesia existe
        if not tipo_anestesia:
            return jsonify({'status': 'error', 'message': 'Tipo de anestesia no encontrado'}), 404
        # Serializar el resultado usando el esquema de tipoanestesia
        return jsonify({
            'status': 'success',
            'data': tipo_anestesia_schema.dump(tipo_anestesia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un tipo de anestesia por nombre
@tiposanestesia_bp.route('/tipos_anestesia/<string:nombre>', methods=['GET'])
def get_tipo_anestesia_by_tipo_anestesia(nombre):
    session = SessionLocal()
    try:
        # Consultar el tipo de anestesia por nombre en la base de datos
        tipo_anestesia = session.query(TipoAnestesia).filter_by(tipo_anestesia=nombre).first()
        # Verificar si el tipo de anestesia existe
        if not tipo_anestesia:
            return jsonify({'status': 'error', 'message': 'Tipo de anestesia no encontrado'}), 404
        # Serializar el resultado usando el esquema de tipoanestesia
        return jsonify({
            'status': 'success',
            'data': tipo_anestesia_schema.dump(tipo_anestesia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear un nuevo tipo de anestesia
@tiposanestesia_bp.route('/tipos_anestesia', methods=['POST'])
def create_tipo_anestesia():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del tipo de anestesia
        if 'tipo_anestesia' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "tipo_anestesia"'}), 400
        
        # Verificar si el tipo de anestesia ya existe en la base de datos
        tipo_anestesia_existente = session.query(TipoAnestesia).filter_by(tipo_anestesia=data['tipo_anestesia']).first()
        if tipo_anestesia_existente:
            return jsonify({'status': 'error', 'message': 'El tipo de anestesia ya existe'}), 400
        
        # Crear una nueva instancia de TipoAnestesia
        nuevo_tipo_anestesia = TipoAnestesia(tipo_anestesia=data['tipo_anestesia'])
        
        # Agregar el nuevo tipo de anestesia a la sesión y confirmar la transacción
        session.add(nuevo_tipo_anestesia)
        session.commit()
        
        # Serializar el resultado usando el esquema de doctipo
        return jsonify({
            'status': 'success',
            'message': 'Tipo de anestesia creado correctamente',
            'data': tipo_anestesia_schema.dump(nuevo_tipo_anestesia)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar un tipo de anestesia por ID
@tiposanestesia_bp.route('/tipos_anestesia/<int:id>', methods=['PUT'])
def update_tipo_anestesia(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del tipo de anestesia
        if 'tipo_anestesia' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "tipo_anestesia"'}), 400
        
        # Consultar el tipo de anestesia por ID en la base de datos
        tipo_anestesia = session.query(TipoAnestesia).get(id)
        
        # Verificar si el tipo de anestesia existe
        if not tipo_anestesia:
            return jsonify({'status': 'error', 'message': 'Tipo de anestesia no encontrado'}), 404
        
        # Verificar si el nuevo tipo de anestesia ya existe en la base de datos
        nuevo_tipo_anestesia_existente = session.query(TipoAnestesia).filter_by(tipo_anestesia=data['tipo_anestesia']).first()
        if nuevo_tipo_anestesia_existente:
            return jsonify({'status': 'error', 'message': 'El tipo de anestesia ya existe'}), 400
        
        # Actualizar el nombre del tipo de anestesia
        tipo_anestesia.tipo_anestesia = data['tipo_anestesia']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de tipoanestesia
        return jsonify({
            'status': 'success',
            'message': 'Tipo de anestesia actualizado correctamente',
            'data': tipo_anestesia_schema.dump(tipo_anestesia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
        
# Ruta para eliminar un tipo de anestesia por ID
@tiposanestesia_bp.route('/tipos_anestesia/<int:id>', methods=['DELETE'])
def delete_tipo_anestesia(id):
    session = SessionLocal()
    try:
        # Consultar el tipo de anestesia por ID en la base de datos
        tipo_anestesia = session.query(TipoAnestesia).get(id)
        # Verificar si el tipo de anestesia existe
        if not tipo_anestesia:
            return jsonify({'status': 'error', 'message': 'Tipo de anestesia no encontrado'}), 404
        # Eliminar el tipo de anestesia de la base de datos
        session.delete(tipo_anestesia)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Tipo de anestesia eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()        
