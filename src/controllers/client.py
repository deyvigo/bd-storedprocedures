from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database import Database

class ClientController:
  @staticmethod
  @jwt_required()
  def get_all_client_info():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_cliente_by_username', [client['username']])
        response = cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo obtener la información del cliente. {e}'}), 500
    finally:
      db.close()

    if not response:
      return jsonify({ 'error': 'Usuario no encontrado' }), 404
    
    del response['password']

    return jsonify(response), 200