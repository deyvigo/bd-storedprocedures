from flask import request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from pydantic import ValidationError
from services.database import Database
from dto.adminCreateDTO import BusCreateDTO
class BusController:
  @staticmethod
  @jwt_required()
  def get_admin_all_bus():
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_bus_all', [])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo recuperar los buses: {e}'}), 400
    finally:
      db.close()

    if not response:
      return jsonify({ 'error': 'No se encontraron buses'}), 404
    
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def admin_create_bus():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      data =BusCreateDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_bus", [data.asientos, data.placa, data.marca, data.niveles,request.json["id_tipo_servicio_bus"],0,0,""])
        cursor.execute("SELECT @_sp_register_bus_4 AS last_id,@_sp_register_bus_6 AS rows_affected,@_sp_register_bus_7 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo registrar el bus. {e}'}), 500
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({
      'message': 'Bus creado exitosamente',
      'id_bus': result['last_id'],
      'asientos': data.asientos,
      'placa': data.placa,
      'marca': data.marca,
      'niveles': data.niveles,
      'id_tipo_servicio_bus': request.json["id_tipo_servicio_bus"]
    }), 201
  
  @staticmethod
  @jwt_required()
  def update_bus(id_bus):
    db = Database().connection()
    try :
      data = BusCreateDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_update_bus_by_id', [
          id_bus,
          data.asientos,
          data.placa,
          data.marca,
          data.niveles,
          request.json["id_tipo_servicio_bus"],
          0,
          ''
        ])
        cursor.execute("""SELECT 
          @_sp_update_bus_by_id_6 AS rows_affected, 
          @_sp_update_bus_by_id_7 AS error_message;
        """)
        result = cursor.fetchall()
        if result and len(result) > 0:
                # Acceder al primer elemento (que debería ser un diccionario)
                first_result = result[0]
                if 'error_message' in first_result and first_result['error_message']:
                    return jsonify({'error': first_result['error_message']}), 400
    except Exception as e:
        return jsonify({'error': f'No se pudo actualizar el bus: {str(e)}'}), 400
    finally:
        db.close()

    return jsonify({'message': 'Bus actualizado'}), 200 