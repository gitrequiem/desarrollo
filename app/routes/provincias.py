from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.provincia import Provincia, ProvinciaSchema

# Crear un blueprint para las rutas de provincias
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
provincias_bp = Blueprint('provincias',__name__)
# Definir esquemas de serialización/deserialización con Marshmallow
provincia_schema = ProvinciaSchema()
provincias_schema = ProvinciaSchema(many=True)

# Ruta para obtener todas las provincias
@provincias_bp.route('/provincias', methods=['GET'])
def get_provincias():
    session = SessionLocal()
    try:
        # Consultar todas las provincias en la base de datos
        provincias = session.query(Provincia).all()
        # Serializar el resultado usando el esquema de provincias
        return jsonify({
            'status': 'success',
            'count': len(provincias),
            'data': provincias_schema.dump(provincias)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una provincia por ID
@provincias_bp.route('/provincias/<int:id>', methods=['GET'])
def get_provincia(id):
    session = SessionLocal()
    try:
        # Consultar la provincia por ID en la base de datos
        provincia = session.query(Provincia).get(id)
        # Verificar si la provincia existe
        if not provincia:
            return jsonify({'status': 'error', 'message': 'Provincia no encontrada'}), 404
        # Serializar el resultado usando el esquema de provincia
        return jsonify({
            'status': 'success',
            'data': provincia_schema.dump(provincia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener una provincia por nombre
@provincias_bp.route('/provincias/<string:nombre>', methods=['GET'])
def get_provincia_by_provincia(nombre):
    session = SessionLocal()
    try:
        # Consultar la provincia por nombre en la base de datos
        provincia = session.query(Provincia).filter_by(provincia=nombre).first()
        # Verificar si la provincia existe
        if not provincia:
            return jsonify({'status': 'error', 'message': 'Provincia no encontrada'}), 404
        # Serializar el resultado usando el esquema de provincia
        return jsonify({
            'status': 'success',
            'data': provincia_schema.dump(provincia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear una nueva provincia
@provincias_bp.route('/provincias', methods=['POST'])
def create_provincia():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la provincia
        if 'provincia' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "provincia"'}), 400
        
        # Verificar si la provincia ya existe en la base de datos
        provincia_existente = session.query(Provincia).filter_by(provincia=data['provincia']).first()
        if provincia_existente:
            return jsonify({'status': 'error', 'message': 'La provincia ya existe'}), 400
        
        # Crear una nueva instancia de Provincia
        nueva_provincia = Provincia(provincia=data['provincia'])
        
        # Agregar la nueva provincia a la sesión y confirmar la transacción
        session.add(nueva_provincia)
        session.commit()
        
        # Serializar el resultado usando el esquema de provincia
        return jsonify({
            'status': 'success',
            'message': 'Provincia creada correctamente',
            'data': provincia_schema.dump(nueva_provincia)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar una provincia por ID
@provincias_bp.route('/provincias/<int:id>', methods=['PUT'])
def update_provincia(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre de la provincia
        if 'provincia' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "provincia"'}), 400
        
        # Consultar la provincia por ID en la base de datos
        provincia = session.query(Provincia).get(id)
        
        # Verificar si la provincia existe
        if not provincia:
            return jsonify({'status': 'error', 'message': 'Provincia no encontrada'}), 404
        
        # Verificar si el nuevo nombre de la provincia ya existe en la base de datos
        nueva_provincia_existente = session.query(Provincia).filter_by(provincia=data['provincia']).first()
        if nueva_provincia_existente:
            return jsonify({'status': 'error', 'message': 'La nueva provincia ya existe'}), 400
        
        # Actualizar el nombre de la provincia
        provincia.provincia = data['provincia']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de provincia
        return jsonify({
            'status': 'success',
            'message': 'Provincia actualizada correctamente',
            'data': provincia_schema.dump(provincia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar una provincia por ID
@provincias_bp.route('/provincias/<int:id>', methods=['DELETE'])
def delete_provincia(id):
    session = SessionLocal()
    try:
        # Consultar la provincia por ID en la base de datos
        provincia = session.query(Provincia).get(id)
        # Verificar si la provincia existe
        if not provincia:
            return jsonify({'status': 'error', 'message': 'Provincia no encontrada'}), 404
        # Eliminar la provincia de la base de datos
        session.delete(provincia)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Provincia eliminada correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
