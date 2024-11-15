from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from dto.discountDTO import DiscountDTO
from services.database import Database

class DiscountController:
  @staticmethod
  @jwt_required()
  def create_discount():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      data = DiscountDTO(**request.json)
    except Exception as e:
      return { 'error': f'No se pudo crear el descuento. {e}' }, 400
    
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_register_descuento', [
          data.codigo, 
          data.monto, 
          data.estado, 
          admin['id_admin'],
          0,
          0,
          ""
        ])
        cursor.execute("SELECT @_sp_create_discount_4 AS rows_affected, @_sp_create_discount_5 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return { 'error': f'No se pudo crear el descuento. {e}' }, 400
    finally:
      db.close()

    if result and result['error_message']:
      return { 'error': result['error_message'] }, 400
    
    return { 'message': 'Descuento creado' }, 201

  @staticmethod
  @jwt_required()
  def get_all_discounts():
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_descuento_all', [])
        response = cursor.fetchall()
    except Exception as e:
      return { 'error': f'No se pudo obtener los descuentos. {e}' }, 400
    finally:
      db.close()

    if not response:
      return { 'error': 'No tienes descuentos' }, 404
    
    return jsonify(response), 200

  @staticmethod
  @jwt_required()
  def edit_discount(id_descuento):
    db = Database().connection()
    admin = get_jwt_identity()
    
    try:
      data = DiscountDTO(**request.json)
    except Exception as e:
      return { 'error': f'No se pudo actualizar el descuento. {e}' }, 400

    try:
      with db.cursor() as cursor:
        rows_affected = 0
        error_message = ''

        cursor.callproc('sp_update_descuento_by_id', [
          id_descuento,
          data.codigo, 
          data.monto, 
          data.estado, 
          admin['id_admin'],
          rows_affected,
          error_message
        ])
        cursor.execute("SELECT @_sp_update_descuento_by_id_5 AS rows_affected, @_sp_update_descuento_by_id_6 AS error_message;")
        result = cursor.fetchone()
        print(result)
        if not result:
          return {'error': 'No se obtuvieron resultados del procedimiento almacenado.'}, 500

        if result['error_message']:
          return jsonify({'error': result['error_message']}), 400

    except Exception as e:
      return { 'error': f'No se pudo actualizar el descuento. {e}' }, 400
    finally:
      db.close()

    return { 'message': 'Descuento actualizado' }, 200
