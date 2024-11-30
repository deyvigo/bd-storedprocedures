from flask import request, jsonify
from flask_jwt_extended import jwt_required

from psycopg2.extras import RealDictCursor

from services.database import Database  
class ControllerGeneral:
  
  @staticmethod
  @jwt_required()
  def get_origins_available():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc('sp_get_origins_available',[])
        response = cursor.fetchall()
        return jsonify(response), 200
    except Exception as e:
      return jsonify({ 'error': 'La base de datos no ha obtenido los datos necesarios' }), 400