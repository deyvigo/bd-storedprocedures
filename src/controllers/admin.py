from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from pydantic import ValidationError
from werkzeug.wrappers import response

from dto.adminDTO import AdminCreateDTO
from services.database import Database


class AdminController:
  @staticmethod
  @jwt_required()
  def get_admin_info():
    db=Database().connection()
    admin = get_jwt_identity()
    print(admin)    

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_get_admin_by_username", [admin['username']])
        response = cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f"No se pudo obtener la info. {e}"}), 500
    finally:
      db.close()

    if not response:
      return jsonify({'error': 'Cliente no encontrado'}, 404)
    
    del response['password']
    return jsonify(response)
