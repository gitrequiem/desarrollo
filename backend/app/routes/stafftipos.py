from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.stafftipo import StaffTipo, StaffTipoSchema

# Crear un blueprint para las rutas de stafftipos
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
stafftipos_bp = Blueprint('staff_tipos', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
staff_tipo_schema = StaffTipoSchema()
staff_tipos_schema = StaffTipoSchema(many=True)

# Ruta para obtener todos los tipos de staff
@stafftipos_bp.route('/staff_tipos', methods=['GET'])
def get_staff_tipos():
    session = SessionLocal()
    try:
        # Consultar todos los tipos de staff en la base de datos
        staff_tipos = session.query(StaffTipo).all()
        # Serializar el resultado usando el esquema de StaffTipo
        return jsonify({
            'status': 'success',
            'count': len(staff_tipos),
            'data': staff_tipos_schema.dump(staff_tipos)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un tipo de staff por ID
@stafftipos_bp.route('/staff_tipos/<int:id>', methods=['GET'])
def get_staff_tipo(id):
    session = SessionLocal()
    try:
        # Consultar el tipo de staff por ID en la base de datos
        staff_tipo = session.query(StaffTipo).get(id)
        # Verificar si el tipo de staff existe
        if not staff_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de staff no encontrado'}), 404
        # Serializar el resultado usando el esquema de stafftipo
        return jsonify({
            'status': 'success',
            'data': staff_tipo_schema.dump(staff_tipo)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un tipo de staff por nombre
@stafftipos_bp.route('/staff_tipos/<string:nombre>', methods=['GET'])
def get_staff_tipo_by_staff_tipo(nombre):
    session = SessionLocal()
    try:
        # Consultar el tipo de staff por nombre en la base de datos
        staff_tipo = session.query(StaffTipo).filter_by(staff_tipo=nombre).first()
        # Verificar si el tipo de staff existe
        if not staff_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de staff no encontrado'}), 404
        # Serializar el resultado usando el esquema de stafftipo
        return jsonify({
            'status': 'success',
            'data': staff_tipo_schema.dump(staff_tipo)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
        
# Ruta para crear un nuevo tipo de staff
@stafftipos_bp.route('/staff_tipos', methods=['POST'])
def create_staff_tipo():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del tipo de staff
        if 'staff_tipo' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "staff_tipo"'}), 400
        
        # Verificar si el tipo de staff ya existe en la base de datos
        staff_tipo_existente = session.query(StaffTipo).filter_by(staff_tipo=data['staff_tipo']).first()
        if staff_tipo_existente:
            return jsonify({'status': 'error', 'message': 'El tipo de staff ya existe'}), 400
        
        # Crear una nueva instancia de StaffTipo
        nuevo_staff_tipo = StaffTipo(staff_tipo=data['staff_tipo'])
        
        # Agregar el nuevo tipo de staff a la sesión y confirmar la transacción
        session.add(nuevo_staff_tipo)
        session.commit()
        
        # Serializar el resultado usando el esquema de doctipo
        return jsonify({
            'status': 'success',
            'message': 'Tipo de staff creado correctamente',
            'data': staff_tipo_schema.dump(nuevo_staff_tipo)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar un tipo de staff por ID
@stafftipos_bp.route('/staff_tipos/<int:id>', methods=['PUT'])
def update_staff_tipo(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del tipo de staff
        if 'staff_tipo' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "staff_tipo"'}), 400
        
        # Consultar el tipo de staff por ID en la base de datos
        staff_tipo = session.query(StaffTipo).get(id)
        
        # Verificar si el tipo de staff existe
        if not staff_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de staff no encontrado'}), 404
        
        # Verificar si el nuevo tipo de staff ya existe en la base de datos
        nuevo_staff_tipo_existente = session.query(StaffTipo).filter_by(staff_tipo=data['staff_tipo']).first()
        if nuevo_staff_tipo_existente:
            return jsonify({'status': 'error', 'message': 'El tipo de staff ya existe'}), 400
        
        # Actualizar el nombre del tipo de staff
        staff_tipo.staff_tipo = data['staff_tipo']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de stafftipo
        return jsonify({
            'status': 'success',
            'message': 'Tipo de staff actualizado correctamente',
            'data': staff_tipo_schema.dump(staff_tipo)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un tipo de staff por ID
@stafftipos_bp.route('/staff_tipos/<int:id>', methods=['DELETE'])
def delete_staff_tipo(id):
    session = SessionLocal()
    try:
        # Consultar el tipo de staff por ID en la base de datos
        staff_tipo = session.query(StaffTipo).get(id)
        # Verificar si el tipo de staff existe
        if not staff_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de staff no encontrado'}), 404
        # Eliminar el tipo de staff de la base de datos
        session.delete(staff_tipo)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Tipo de staff eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()