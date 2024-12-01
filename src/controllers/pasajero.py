from flask import jsonify, request
from flask_jwt_extended import jwt_required

from dto.pasajeroDTO import PasajeroDTO
from services.database import Database

class PasajeroController:
  @staticmethod
  @jwt_required()
  def create_pasajero():
    db = Database().connection()

    try:
      data = PasajeroDTO(**request.json)
    except Exception as e:
      return {'error': f'Error al procesar el pasajero: {e}'}, 400

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_register_pasajero', [
          data.dni,
          data.nombre,
          data.apellido_pat,
          data.apellido_mat,
          data.fecha_nacimiento,
          data.sexo,
          0,
          0,
          ''
        ])
        cursor.execute("""SELECT 
          @_sp_register_pasajero_6 AS last_id, 
          @_sp_register_pasajero_7AS rows_affected, 
          @_sp_register_pasajero_8 AS error_message;
        """)
        result = cursor.fetchone()
    except Exception as e:
      return {'error': f'No se pudo registrar el pasajero: {e}'}, 400
    finally:
      db.close()

    if result and result['error_message']:
      return {'error': result['error_message']}, 400
    
    print(result)
    return jsonify({
      'message': 'Pasajero registrado',
      'id_pasajero': result['last_id'],
    }), 201
