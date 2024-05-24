from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.staff import Staff, StaffSchema
from app.models.stafftipo import StaffTipo

# Crear un blueprint para las rutas de staffs
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
staffs_bp = Blueprint('staff', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
staff_schema = StaffSchema()
staffs_schema = StaffSchema(many=True)

# Ruta para obtener todos los staffs
@staffs_bp.route('/staff', methods=['GET'])
def get_staffs():
    session = SessionLocal()
    try:
        # Consultar todos los staffs en la base de datos
        staffs = session.query(Staff).all()
        # Serializar el resultado usando el esquema de Staff
        return jsonify({
            'status': 'success',
            'count': len(staffs),
            'data': staffs_schema.dump(staffs)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un staff por ID
@staffs_bp.route('/staff/<int:id>', methods=['GET'])
def get_staff(id):
    session = SessionLocal()
    try:
        # Consultar un staff por ID en la base de datos
        staff = session.query(Staff).get(id)
        # Verificar si el staff existe
        if not staff:
            return jsonify({'status': 'error', 'message': 'Staff no encontrado'}), 404
        # Serializar el resultado usando el esquema de staff
        return jsonify({
            'status': 'success',
            'data': staff_schema.dump(staff)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para obtener un staff por nombre
@staffs_bp.route('/staff/<string:nombre>', methods=['GET'])
def get_staff_by_staff(nombre):
    session = SessionLocal()
    try:
        # Construcción de query para buscar por apellidos o nombres de staff
        staff = session.query(Staff).filter(
            Staff.apellidos.like('%' + nombre + '%') |
            Staff.nombres.like('%' + nombre + '%')
        ).first()
        
        # Verifica si el staff existe
        if not staff:
            return jsonify({'status':'error', 'message': 'Staff no existente.'})
        
        return jsonify({
            'status': 'success',
            'data': staff_schema.dump(staff)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear un nuevo staff
@staffs_bp.route('/staff', methods=['POST'])
def create_staff():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporcionan los apellidos del staff
        if 'apellidos' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "apellidos"'}), 400
        # Validar si se proporcionan los nombres del staff
        if 'nombres' not in data:
            return jsonify({'status':'error', 'message': 'Falta campo "nombres"'}), 400
        # Validar si se proporciona el id_staff_tipo del staff
        if 'id_staff_tipo' not in data:
            return jsonify({'status': 'error', 'message':'Falta campo "id_staff_tipo"'}),400
        
        # Validar el largo de apellidos
        if len(data['apellidos']) < 1 or len(data['apellidos']) > 60:
            return jsonify({'status':'error', 'message': 'Los apellidos deben tener entre 1 y 60 caracteres'}), 400
        
        # Validar el largo de nombres
        if len(data['nombres']) < 1 or len(data['nombres']) > 60:
            return jsonify({'status':'error', 'message':'Los nombres deben tener entre 1 y 60 caracteres'}), 400
        
        # Verificar si existe staff (apellidos + nombres)
        staff_existente = session.query(Staff).filter_by(apellidos=data['apellidos'], nombres=data['nombres']).first()
        if staff_existente:
            return jsonify({'status':'error','message':'El staff ya existe'}),400

        # Verificar si el id_staff_tipo existe en la tabla staff_tipos
        staff_tipo_existente = session.query(StaffTipo).get(data['id_staff_tipo'])
        if not staff_tipo_existente:
            return jsonify({'status':'error', 'message': 'El tipo de staff no existe'}), 400
        
        # Crear una nueva instancia de Staff
        nuevo_staff = Staff(apellidos=data['apellidos'], nombres=data['nombres'], id_staff_tipo=data['id_staff_tipo'])
        
        # Agregar el nuevo staff a la sesión y confirmar la transacción
        session.add(nuevo_staff)
        session.commit()
        
        # Serializar el resultado usando el esquema de staff
        return jsonify({
            'status': 'success',
            'message': 'Staff creado correctamente',
            'data': staff_schema.dump(nuevo_staff)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar un staff por ID
@staffs_bp.route('/staff/<int:id>', methods=['PUT'])
def update_staff(id):
    session = SessionLocal()
    try:
        # Recupera Staff por el ID
        staff = session.query(Staff).filter_by(id_staff=id).first()
        if not staff:
            return jsonify({'status':'error', 'message':'Staff no encontrado'}), 400
        
        data = request.json
        # Validar si se proporcionan los apellidos del staff
        if 'apellidos' not in data or 'nombres' not in data:
            return jsonify({'status':'error', 'message':'No se encuentra ese apellido y/o nombre'}), 400
        
        # Validar si apellidos y nombres son únicos
        nuevo_staff_nombre = data['apellidos'] + ' ' + data['nombres']
        staff_existente = session.query(Staff).filter(
            Staff.apellidos == data['apellidos'],
            Staff.nombres == data['nombres'],
            Staff.id_staff != id 
        ).one_or_none()
        if staff_existente:
            return jsonify({'status':'error', 'message':'Ya existe un staff con ese nombre y apellido'}), 400
        
        # Valida si esta el id_staff_tipo en la tabla Staff_tipos
        if 'id_staff_tipo' in data:
            staff_tipo = session.query(StaffTipo).filter_by(id_staff_tipo=data['id_staff_tipo']).first()
            if not staff_tipo:
                return jsonify({'status':'error', 'message':'id_staff_tipo Inválido'}), 400
            staff.id_staff_tipo = data['id_staff_tipo']
        
        # Modifica los datos del staff seleccionado
        staff.apellidos = data['apellidos']
        staff.nombres = data['nombres']
        if 'id_staff_tipo' in data:
            staff.id_staff_tipo = data['id_staff_tipo']
        
        # Confirmar la transacción
        session.commit()
         # Serializar el resultado usando el esquema de diagnostico
        return jsonify({
            'status': 'success',
            'message': 'Staff actualizado correctamente',
            'data': staff_schema.dump(staff)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un staff por ID
@staffs_bp.route('/staff/<int:id>', methods=['DELETE'])
def delete_staff(id):
    session = SessionLocal()
    try:
        # Consultar staff por ID en la base de datos
        staff = session.query(Staff).get(id)
        # Verificar si el staff existe
        if not staff:
            return jsonify({'status': 'error', 'message': 'Staff no encontrado'}), 404
        # Eliminar el staff de la base de datos
        session.delete(staff)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Staff eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()