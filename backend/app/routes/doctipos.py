from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.configs.database import SessionLocal
from app.models.doctipo import DocTipo, DocTipoSchema

# Crear un blueprint para las rutas de doctipos
# Los blueprints permiten organizar y desacoplar las rutas en módulos.
doctipos_bp = Blueprint('doc_tipos', __name__)
# Definir esquemas de serialización/deserialización con Marshmallow
doc_tipo_schema = DocTipoSchema()
doc_tipos_schema = DocTipoSchema(many=True)

# Ruta para obtener todos los tipos de documento
@doctipos_bp.route('/doc_tipos', methods=['GET'])
def get_doc_tipos():
    session = SessionLocal()
    try:
        # Consultar todos los tipos de documento en la base de datos
        doc_tipos = session.query(DocTipo).all()
        # Serializar el resultado usando el esquema de DocTipo
        return jsonify({
            'status': 'success',
            'count': len(doc_tipos),
            'data': doc_tipos_schema.dump(doc_tipos)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
            session.close()

# Ruta para obtener un tipo de documento por ID
@doctipos_bp.route('/doc_tipos/<int:id>', methods=['GET'])
def get_doc_tipo(id):
    session = SessionLocal()
    try:
        # Consultar el tipo de documento por ID en la base de datos
        doc_tipo = session.query(DocTipo).get(id)
        # Verificar si el tipo de documento existe
        if not doc_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de documento no encontrado'}), 404
        # Serializar el resultado usando el esquema de doctipo
        return jsonify({
            'status': 'success',
            'data': doc_tipo_schema.dump(doc_tipo)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()
        
# Ruta para obtener un tipo de documento por nombre
@doctipos_bp.route('/doc_tipos/<string:nombre>', methods=['GET'])
def get_doc_tipo_by_doc_tipo(nombre):
    session = SessionLocal()
    try:
        # Consultar el tipo de documento por nombre en la base de datos
        doc_tipo = session.query(DocTipo).filter_by(doc_tipo=nombre).first()
        # Verificar si el tipo de documento existe
        if not doc_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de documento no encontrado'}), 404
        # Serializar el resultado usando el esquema de doctipo
        return jsonify({
            'status': 'success',
            'data': doc_tipo_schema.dump(doc_tipo)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para crear un nuevo tipo de documento
@doctipos_bp.route('/doc_tipos', methods=['POST'])
def create_doc_tipo():
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del tipo de documento
        if 'doc_tipo' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "doc_tipo"'}), 400
        
        # Verificar si el tipo de documento ya existe en la base de datos
        doc_tipo_existente = session.query(DocTipo).filter_by(doc_tipo=data['doc_tipo']).first()
        if doc_tipo_existente:
            return jsonify({'status': 'error', 'message': 'El tipo de documento ya existe'}), 400
        
        # Crear una nueva instancia de DocTipo
        nuevo_doc_tipo = DocTipo(doc_tipo=data['doc_tipo'])
        
        # Agregar el nuevo tipo de documento a la sesión y confirmar la transacción
        session.add(nuevo_doc_tipo)
        session.commit()
        
        # Serializar el resultado usando el esquema de doctipo
        return jsonify({
            'status': 'success',
            'message': 'Tipo de documento creado correctamente',
            'data': doc_tipo_schema.dump(nuevo_doc_tipo)
        }), 201
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para actualizar un tipo de documento por ID
@doctipos_bp.route('/doc_tipos/<int:id>', methods=['PUT'])
def update_doc_tipo(id):
    session = SessionLocal()
    try:
        data = request.json
        # Validar si se proporciona el nombre del tipo de documento
        if 'doc_tipo' not in data:
            return jsonify({'status': 'error', 'message': 'Falta el campo "doc_tipo"'}), 400
        
        # Consultar el tipo de documento por ID en la base de datos
        doc_tipo = session.query(DocTipo).get(id)
        
        # Verificar si el tipo de documento existe
        if not doc_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de documento no encontrado'}), 404
        
        # Verificar si el nuevo tipo de documento ya existe en la base de datos
        nuevo_doc_tipo_existente = session.query(DocTipo).filter_by(doc_tipo=data['doc_tipo']).first()
        if nuevo_doc_tipo_existente:
            return jsonify({'status': 'error', 'message': 'El tipo de documento ya existe'}), 400
        
        # Actualizar el nombre del tipo de documento
        doc_tipo.doc_tipo = data['doc_tipo']
        
        # Confirmar la transacción
        session.commit()
        
        # Serializar el resultado usando el esquema de doctipo
        return jsonify({
            'status': 'success',
            'message': 'Tipo de documento actualizado correctamente',
            'data': doc_tipo_schema.dump(doc_tipo)
        }), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()

# Ruta para eliminar un tipo de documento por ID
@doctipos_bp.route('/doc_tipos/<int:id>', methods=['DELETE'])
def delete_doc_tipo(id):
    session = SessionLocal()
    try:
        # Consultar el tipo de documento por ID en la base de datos
        doc_tipo = session.query(DocTipo).get(id)
        # Verificar si el tipo de documento existe
        if not doc_tipo:
            return jsonify({'status': 'error', 'message': 'Tipo de documento no encontrado'}), 404
        # Eliminar el tipo de documento de la base de datos
        session.delete(doc_tipo)
        # Confirmar la transacción
        session.commit()
        # Devolver un mensaje de éxito
        return jsonify({'status': 'success', 'message': 'Tipo de documento eliminado correctamente'}), 200
    except SQLAlchemyError as e:
        # Manejo de errores de SQLAlchemy
        session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500
    finally:
        session.close()