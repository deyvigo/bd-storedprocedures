from flask import request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from pydantic import ValidationError
from services.database import Database
from dto.adminCreateDTO import RutaDTO
from datetime import timedelta

class RutaController:
  @staticmethod
  @jwt_required()
  def admin_create_route():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      data = RutaDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400
    
    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_ruta", [data.duracion_estimada.strftime('%H:%M:%S'), data.distancia, data.estado, data.id_origen,data.id_destino, 0, 0, ''])
        cursor.execute("SELECT @_sp_register_ruta_5 AS last_id,@_sp_register_ruta_6 AS rows_affected,@_sp_register_ruta_7 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo registrar la ruta. {e}'}), 500
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({
      'message': 'Ruta creada exitosamente',
      'id_ruta': result['last_id'],
      'duracion_estimada': data.duracion_estimada.strftime('%H:%M:%S'),
      'distancia': data.distancia,
      'estado': data.estado,
      'id_origen': data.id_origen ,
      'id_destino': data.id_destino
    }), 201
  
  @staticmethod
  @jwt_required()
  def get_ruta_all():
    admin = get_jwt_identity()
    db = Database().connection()
    try:
        with db.cursor() as cursor:
            cursor.callproc("sp_get_ruta_all")
            response = cursor.fetchall()
            # Convertir timedelta en cadenas
            for row in response:
                if 'duracion_estimada' in row and isinstance(row['duracion_estimada'], timedelta):
                    row['duracion_estimada'] = str(row['duracion_estimada'])
    except Exception as e:
        return jsonify({'error': f'No se pudo recuperar las rutas: {e}'}), 400
    finally:
        db.close()

    if not response:
        return jsonify({'error': 'No se encontraron rutas'}), 404
    
    return jsonify(response), 200


  @staticmethod
  @jwt_required()
  def update_ruta(id_ruta):
    db=Database().connection()
    try:
      data = RutaDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_update_ruta_by_id", [id_ruta,data.duracion_estimada.strftime('%H:%M:%S'), data.distancia, data.estado, data.id_origen,data.id_destino, 0, ''])
        cursor.execute("""SELECT @_sp_update_ruta_6 AS rows_affected,@_sp_update_ruta_7 AS error_message;""")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo actualizar la ruta. {e}'}), 400
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    return jsonify({  'message': 'Ruta actualizada exitosamente' }), 200
