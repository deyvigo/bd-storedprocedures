from flask import request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from pydantic import ValidationError
from services.database import Database
from dto.adminCreateDTO import AsientoDTO
class AsientoController:
  @staticmethod
  @jwt_required()
  def admin_create_asiento():
    admin = get_jwt_identity()
    db=Database().connection()

    try:
      data=AsientoDTO(**request.json)
    except ValidationError as ve:
      return jsonify({'error': ve.errors()}),400
    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_asiento",[data.nivel,data.numero,request.json["id_bus"],0,0,''])
        cursor.execute("SELECT @_sp_register_asiento_3 AS last_id,@_sp_register_asiento_4 AS rows_affected,@_sp_register_asiento_5 AS error_message;")
        result=cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo registrar el asiento. {e}'}),500
    finally:
      db.close()

    if result and result['error_message']:
      return jsonify({'error': result['error_message']}),400

    return jsonify({
      'message':'Asiento creado exitosamente',
      'id_asiento':result['last_id'],
      'nivel':data.nivel,
      'numero':data.numero,
      'id_bus':request.json["id_bus"]
    }),201  

  @staticmethod
  @jwt_required()
  def admin_get_asiento():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_get_asiento_all",[])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo obtener la lista de asientos. {e}'}), 500
    finally:
      db.close()
    if not response:
      return jsonify({ 'error': 'No tienes métodos de pago' }), 404

    return jsonify(response), 200
  @staticmethod
  @jwt_required()
  def update_asiento(id_asiento):
    db=Database().connection()
    try:
      data=AsientoDTO(**request.json)
    except ValidationError as ve:
      return jsonify({'error': ve.errors()}),400

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_update_asiento_by_id",[id_asiento,data.nivel,data.numero,request.json["id_bus"],0,''])
        cursor.execute("""SELECT @_sp_update_asiento_by_id_4 AS rows_affected,@_sp_update_asiento_by_id_5 AS error_message;""")
        result=cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f'No se pudo actualizar el asiento. {e}'}),500
    finally:
      db.close()
    return jsonify({
      'message':'Asiento actualizado exitosamente'
    }),200