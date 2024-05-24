from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.nacionalidad import Nacionalidad, NacionalidadSchema

# Crear un blueprint para las rutas de nacionalidades
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
nacionalidades_bp = Blueprint('nacionalidades', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
nacionalidad_schema = NacionalidadSchema()
nacionalidades_schema = NacionalidadSchema(many=True)

# Ruta para obtener todas las nacionalidades
@nacionalidades_bp.route('/nacionalidades', methods=['GET'])
def get_nacionalidades():
    """
    Endpoint para obtener todas las nacionalidades.

    Returns:
        JSON: Lista de nacionalidades.
    """
    session = SessionLocal()
    try:
        # Consultar todas las nacionalidades en la base de datos
        nacionalidades = session.query(Nacionalidad).all()
        # Serializar el resultado usando el esquema de nacionalidades
        return jsonify({
            'status': 'success',
            'count': len(nacionalidades),
            'data': nacionalidades_schema.dump(nacionalidades)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una nacionalidad por ID
@nacionalidades_bp.route('/nacionalidades/<int:id>', methods=['GET'])
def get_nacionalidad(id):
    """
    Endpoint para obtener una nacionalidad por ID.

    Args:
        id (int): ID de la nacionalidad.

    Returns:
        JSON: Detalles de la nacionalidad.
    """
    session = SessionLocal()
    try:
        # Consultar la nacionalidad por ID en la base de datos
        nacionalidad = session.query(Nacionalidad).get(id)
        # Verificar si la nacionalidad existe
        if not nacionalidad:
            return jsonify({'status': 'error', 'message': 'Nacionalidad no encontrada'}), 404
        # Serializar el resultado usando el esquema de nacionalidad
        return jsonify({
            'status': 'success',
            'data': nacionalidad_schema.dump(nacionalidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una nacionalidad por nombre
@nacionalidades_bp.route('/nacionalidades/<string:nombre>', methods=['GET'])
def get_nacionalidad_by_nacionalidad(nombre):
    """
    Endpoint para obtener una nacionalidad por nombre.

    Args:
        nombre (str): Nombre de la nacionalidad.

    Returns:
        JSON: Detalles de la nacionalidad.
    """
    session = SessionLocal()
    try:
        # Consultar la nacionalidad por nombre en la base de datos
        nacionalidad = session.query(Nacionalidad).filter_by(nacionalidad=nombre).first()
        # Verificar si la nacionalidad existe
        if not nacionalidad:
            return jsonify({'status': 'error', 'message': 'Nacionalidad no encontrada'}), 404
        # Serializar el resultado usando el esquema de nacionalidad
        return jsonify({
            'status': 'success',
            'data': nacionalidad_schema.dump(nacionalidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear una nueva nacionalidad
@nacionalidades_bp.route('/nacionalidades', methods=['POST'])
def create_nacionalidad():
    """
    Endpoint para crear una nueva nacionalidad.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la nacionalidad
        if 'nacionalidad' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "nacionalidad"'}), 400
        
        # Verificar si la nacionalidad ya existe en la base de datos
        nacionalidad_existente = session.query(Nacionalidad).filter_by(nacionalidad=data['nacionalidad']).first()
        if nacionalidad_existente:
            return jsonify({'status': 'error', 'message': 'La nacionalidad ya existe'}), 400
        
        # Crear una nueva instancia de Nacionalidad
        nueva_nacionalidad = Nacionalidad(nacionalidad=data['nacionalidad'])
        
        # Agregar la nueva nacionalidad a la sesión y confirmar la transacción
        session.add(nueva_nacionalidad)
        session.commit()
        
        # Serializar el resultado usando el esquema de nacionalidad
        return jsonify({
            'status': 'success',
            'message': 'Nacionalidad creada correctamente',
            'data': nacionalidad_schema.dump(nueva_nacionalidad)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar una nacionalidad por ID
@nacionalidades_bp.route('/nacionalidades/<int:id>', methods=['PUT'])
def update_nacionalidad(id):
    """
    Endpoint para actualizar una nacionalidad por ID.

    Args:
        id (int): ID de la nacionalidad.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la nacionalidad
        if 'nacionalidad' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "nacionalidad"'}), 400
        
        # Consultar la nacionalidad por ID en la base de datos
        nacionalidad = session.query(Nacionalidad).get(id)
        
        # Verificar si la nacionalidad existe
        if not nacionalidad:
            return jsonify({'status': 'error', 'message': 'Nacionalidad no encontrada'}), 404
        
        # Verificar si el nuevo nombre de la nacionalidad ya existe en la base de datos
        nueva_nacionalidad_existente = session.query(Nacionalidad).filter_by(nacionalidad=data['nacionalidad']).first()
        if nueva_nacionalidad_existente:
            return jsonify({'status': 'error', 'message': 'La nueva nacionalidad ya existe'}), 400
        
        # Actualizar el nombre de la nacionalidad
        nacionalidad.nacionalidad = data['nacionalidad']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de nacionalidad
        return jsonify({
            'status': 'success',
            'message': 'Nacionalidad actualizada correctamente',
            'data': nacionalidad_schema.dump(nacionalidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()


# Ruta para eliminar una nacionalidad por ID
@nacionalidades_bp.route('/nacionalidades/<int:id>', methods=['DELETE'])
def delete_nacionalidad(id):
    """
    Endpoint para eliminar una nacionalidad por ID.

    Args:
        id (int): ID de la nacionalidad.

    Returns:
        JSON: Mensaje de éxito o error.
    """
    session = SessionLocal()
    try:
        # Consultar la nacionalidad por ID en la base de datos
        nacionalidad = session.query(Nacionalidad).get(id)
        # Verificar si la nacionalidad existe
        if not nacionalidad:
            return jsonify({'status': 'error', 'message': 'Nacionalidad no encontrada'}), 404
        # Eliminar la nacionalidad de la base de datos
        session.delete(nacionalidad)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Nacionalidad eliminada correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
