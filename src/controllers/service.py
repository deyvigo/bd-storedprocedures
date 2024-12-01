from flask import jsonify, request

from flask_jwt_extended import jwt_required

from dto.serviceDTO import ServiceDTO
from services.database import Database

class ServiceController:
  @staticmethod
  @jwt_required()
  def get_all_services():
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_tipo_servicio_bus_all', [])
        response = cursor.fetchall()
    except Exception as e:
      return {'error': f'No se pudo recuperar los servicios: {e}'}, 400
    finally:
      db.close()

    if not response:
      return {'error': 'No se encontraron servicios'}, 404
    
    return jsonify(response), 200

  @staticmethod
  @jwt_required()
  def create_service():
    db = Database().connection()

    try:
      data = ServiceDTO(**request.json)
    except Exception as e:
      return {'error': f'Error al procesar el servicio: {e}'}, 400

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_register_tipo_servicio_bus', [
          data.servicio,
          0,
          0,
          ""
        ])
        cursor.execute("""SELECT 
          @_sp_create_tipo_servicio_bus_2 AS rows_affected, 
          @_sp_create_tipo_servicio_bus_3 AS error_message;
        """)
        result = cursor.fetchone()
    except Exception as e:
      return {'error': f'No se pudo crear el servicio: {e}'}, 400
    finally:
      db.close()

    if result and result['error_message']:
      return {'error': result['error_message']}, 400

    return {'message': 'Servicio creado'}, 201

  @staticmethod
  @jwt_required()
  def edit_service(id_servicio):
    db = Database().connection()

    try:
      data = ServiceDTO(**request.json)
    except Exception as e:
      return {'error': f'Error al procesar el servicio: {e}'}, 400
    
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_update_tipo_servicio_bus_by_id', [
          id_servicio,
          data.servicio,
          0,
          ''
        ])
        cursor.execute("""SELECT 
          @_sp_update_tipo_servicio_bus_by_id_2 AS rows_affected, 
          @_sp_update_tipo_servicio_bus_by_id_3 AS error_message;
        """)
        result = cursor.fetchone()
    except Exception as e:
      return {'error': f'No se pudo recuperar los servicios: {e}'}, 400
    finally:
      db.close()

    if result and result['error_message']:
      return {'error': result['error_message']}, 400

    return {'message': 'Servicio actualizado'}, 200
