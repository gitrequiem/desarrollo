from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.localidad import Localidad, LocalidadSchema
from app.models.provincia import Provincia

# Crear un blueprint para las rutas de localidades
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
localidades_bp = Blueprint('localidades', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
localidad_schema = LocalidadSchema()
localidades_schema = LocalidadSchema(many=True)

# Ruta para obtener todos las localidades
@localidades_bp.route('/localidades', methods=['GET'])
def get_localidades():
    session = SessionLocal()
    try:
        # Consultar todos las localidades en la base de datos
        localidades = session.query(Localidad).all()
        # Serializar el resultado usando el esquema de Localidad
        return jsonify({
            'status': 'success',
            'count': len(localidades),
            'data': localidades_schema.dump(localidades)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener una localidad por ID
@localidades_bp.route('/localidades/<int:id>', methods=['GET'])
def get_localidad(id):
    session = SessionLocal()
    try:
        # Consultar la localidad por ID en la base de datos
        localidad = session.query(Localidad).get(id)
        # Verificar si la localidad existe
        if not localidad:
            return jsonify({'status': 'error', 'message': 'Localidad no encontrado'}), 404
        # Serializar el resultado usando el esquema de localidad
        return jsonify({
            'status': 'success',
            'data': localidad_schema.dump(localidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una localidad por nombre
@localidades_bp.route('/localidades/<string:nombre>', methods=['GET'])
def get_localidad_by_localidad(nombre):
    session = SessionLocal()
    try:
        # Consultar la localidad por nombre en la base de datos
        localidad = session.query(Localidad).filter_by(localidad=nombre).first()
        # Verificar si la localidad existe
        if not localidad:
            return jsonify({'status': 'error', 'message': 'Localidad no encontrado'}), 404
        # Serializar el resultado usando el esquema de localidad
        return jsonify({
            'status': 'success',
            'data': localidad_schema.dump(localidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear una nueva localidad
@localidades_bp.route('/localidades', methods=['POST'])
def create_localidad():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la localidad
        if 'localidad' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "localidad"'}), 400
        
        # Verificar si la localidad ya existe en la base de datos
        localidad_existente = session.query(Localidad).filter_by(localidad=data['localidad']).first()
        if localidad_existente:
            return jsonify({'status': 'error', 'message': 'La localidad ya existe'}), 400
        
        
        # Validar si se proporcion el id_provincia
        if 'id_provincia' not in data:
            return jsonify({'status':'error', 'message': 'Falta campo "id_provincia"'}),400
        
        # Verificar si el id_provincia existe en la tabla provincias
        provincia_existente = session.query(Provincia).get(data['id_provincia'])
        if not provincia_existente:
            return jsonify({'status':'error', 'message': 'La provincia no existe'}), 400
        
        # Crear una nueva instancia de Localidad
        nueva_localidad = Localidad(localidad=data['localidad'], id_provincia=data['id_provincia'])
        
        # Agregar la nueva localidad a la sesión y confirmar la transacción
        session.add(nueva_localidad)
        session.commit()
        
        # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'message': 'Localidad creada correctamente',
            'data': localidad_schema.dump(nueva_localidad)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
        
# Ruta para actualizar una localidad por ID
@localidades_bp.route('/localidades/<int:id>', methods=['PUT'])
def update_localidad(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la localidad
        if 'localidad' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "localidad"'}), 400
        
        # Consultar la localidad por ID en la base de datos
        localidad = session.query(Localidad).get(id)
        
        # Verificar si la localidad existe
        if not localidad:
            return jsonify({'status': 'error', 'message': 'Localidad no encontrada'}), 404
        
        # Verificar si la nueva localidad ya existe en la base de datos
        nueva_localidad_existente = session.query(Localidad).filter_by(localidad=data['localidad']).first()
        if nueva_localidad_existente:
            return jsonify({'status': 'error', 'message': 'La localidad ya existe'}), 400
        
        # Actualizar el nombre de la localidad
        localidad.localidad = data['localidad']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de localidad
        return jsonify({
            'status': 'success',
            'message': 'Localidad actualizada correctamente',
            'data': localidad_schema.dump(localidad)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar una localidad por ID
@localidades_bp.route('/localidades/<int:id>', methods=['DELETE'])
def delete_localidad(id):
    session = SessionLocal()
    try:
        # Consultar la localidad por ID en la base de datos
        localidad = session.query(Localidad).get(id)
        # Verificar si la localidad existe
        if not localidad:
            return jsonify({'status': 'error', 'message': 'Localidad no encontrada'}), 404
        # Eliminar la localidad de la base de datos
        session.delete(localidad)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Localidad eliminada correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()