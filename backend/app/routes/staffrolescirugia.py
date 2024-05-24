from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.staffrolcirugia import StaffRolCirugia, StaffRolCirugiaSchema

# Crear un blueprint para las rutas de staffrolescirugia
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
staffrolescirugia_bp = Blueprint('staff_roles_cirugia', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
staff_rol_cirugia_schema = StaffRolCirugiaSchema()
staff_roles_cirugia_schema = StaffRolCirugiaSchema(many=True)

# Ruta para obtener todos los staff roles cirugia
@staffrolescirugia_bp.route('/staff_roles_cirugia', methods=['GET'])
def get_staff_roles_cirugia():
    session = SessionLocal()
    try:
        # Consultar todos los staff roles cirugia en la base de datos
        staff_roles_cirugia = session.query(StaffRolCirugia).all()
        # Serializar el resultado usando el esquema de StaffRolCirugia
        return jsonify({
            'status': 'success',
            'count': len(staff_roles_cirugia),
            'data': staff_roles_cirugia_schema.dump(staff_roles_cirugia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un tipo de staff rol cirugia por ID
@staffrolescirugia_bp.route('/staff_roles_cirugia/<int:id>', methods=['GET'])
def get_staff_rol_cirugia(id):
    session = SessionLocal()
    try:
        # Consultar el staff rol cirugia por ID en la base de datos
        staff_rol_cirugia = session.query(StaffRolCirugia).get(id)
        # Verificar si staff rol cirugia existe
        if not staff_rol_cirugia:
            return jsonify({'status': 'error', 'message': 'Staff rol cirugía no encontrado'}), 404
        # Serializar el resultado usando el esquema de staffrolcirugia
        return jsonify({
            'status': 'success',
            'data': staff_rol_cirugia_schema.dump(staff_rol_cirugia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un staff rol cirugia por nombre
@staffrolescirugia_bp.route('/staff_roles_cirugia/<string:nombre>', methods=['GET'])
def get_staff_rol_cirugia_by_staff_rol_cirugia(nombre):
    session = SessionLocal()
    try:
        # Consultar el staff rol cirugia por nombre en la base de datos
        staff_rol_cirugia = session.query(StaffRolCirugia).filter_by(staff_rol_cirugia=nombre).first()
        # Verificar si el staff rol cirugia existe
        if not staff_rol_cirugia:
            return jsonify({'status': 'error', 'message': 'Staff rol cirugía no encontrado'}), 404
        # Serializar el resultado usando el esquema de staffrolcirugia
        return jsonify({
            'status': 'success',
            'data': staff_rol_cirugia_schema.dump(staff_rol_cirugia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear un nuevo staff rol cirugia
@staffrolescirugia_bp.route('/staff_roles_cirugia', methods=['POST'])
def create_staff_rol_cirugia():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del staff rol cirugia
        if 'rol_cirugia' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "rol_cirugia"'}), 400
        
        # Verificar si el staff rol cirugia ya existe en la base de datos
        rol_cirugia_existente = session.query(StaffRolCirugia).filter_by(rol_cirugia=data['rol_cirugia']).first()
        if rol_cirugia_existente:
            return jsonify({'status': 'error', 'message': 'El staff rol cirugía ya existe'}), 400
        
        # Crear una nueva instancia de StaffRolCirugia
        nuevo_rol_cirugia = StaffRolCirugia(rol_cirugia=data['rol_cirugia'])
        
        # Agregar el nuevo tipo de documento a la sesión y confirmar la transacción
        session.add(nuevo_rol_cirugia)
        session.commit()
        
        # Serializar el resultado usando el esquema de staffrolcirugia
        return jsonify({
            'status': 'success',
            'message': 'Staff rol cirugía creado correctamente',
            'data': staff_rol_cirugia_schema.dump(nuevo_rol_cirugia)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar un staff rol cirugia por ID
@staffrolescirugia_bp.route('/staff_roles_cirugia/<int:id>', methods=['PUT'])
def update_staff_rol_cirugia(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del staff rol cirugia
        if 'rol_cirugia' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "rol_cirugia"'}), 400
        
        # Consultar el staff rol cirugia por ID en la base de datos
        rol_cirugia = session.query(StaffRolCirugia).get(id)
        
        # Verificar si el staff rol cirugia existe
        if not rol_cirugia:
            return jsonify({'status': 'error', 'message': 'Staff rol cirugía no encontrado'}), 404
        
        # Verificar si el nuevo staff rol cirugia ya existe en la base de datos
        nuevo_rol_cirugia_existente = session.query(StaffRolCirugia).filter_by(rol_cirugia=data['rol_cirugia']).first()
        if nuevo_rol_cirugia_existente:
            return jsonify({'status': 'error', 'message': 'El staff rol cirugía ya existe'}), 400
        
        # Actualizar el nombre del staff rol cirugia
        rol_cirugia.rol_cirugia = data['rol_cirugia']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de staffrolcirugia
        return jsonify({
            'status': 'success',
            'message': 'Staff rol cirugía actualizado correctamente',
            'data': staff_rol_cirugia_schema.dump(rol_cirugia)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un staff rol cirugia por ID
@staffrolescirugia_bp.route('/staff_roles_cirugia/<int:id>', methods=['DELETE'])
def delete_staff_rol_cirugia(id):
    session = SessionLocal()
    try:
        # Consultar el staff rol cirugia por ID en la base de datos
        rol_cirugia = session.query(StaffRolCirugia).get(id)
        # Verificar si el staff rol cirugia existe
        if not rol_cirugia:
            return jsonify({'status': 'error', 'message': 'Staff rol cirugía no encontrado'}), 404
        # Eliminar el staff rol cirugia de la base de datos
        session.delete(rol_cirugia)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Staff rol cirugía eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()