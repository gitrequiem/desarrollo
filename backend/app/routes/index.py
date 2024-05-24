from flask import Blueprint, jsonify

index_bp = Blueprint('/', __name__)

@index_bp.route('/')
def index():
    return jsonify({"message": "¡Bienvenido a REQUIEM!"})
