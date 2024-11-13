from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from services.database import Database
from dto.metodo_pago import MetodoPagoCreateDTO

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
  
  @staticmethod
  @jwt_required()
  def get_all_client_payment_methods():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_metodo_pago_all_active_by_id_client', [client['id_cliente']])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f'No se pudo obtener los métodos de pago del cliente. {e}'}), 500
    finally:
      db.close()

    if not response:
      return jsonify({ 'error': 'No tienes métodos de pago' }), 404
    
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def delete_client_payment_method(id_metodo_pago):
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_delete_metodo_pago_by_id', [id_metodo_pago, 0, ''])
        cursor.execute("SELECT @_sp_delete_metodo_pago_by_id_1 AS rows_affected, @_sp_delete_metodo_pago_by_id_2 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo eliminar el método de pago. {e}'}), 500
    finally:
      db.close()

    if result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({ 'message': 'Método de pago eliminado' }), 200
  
  @staticmethod
  @jwt_required()
  def create_client_payment_method():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      data = MetodoPagoCreateDTO(**request.json)
    except ValidationError as ve:
      return jsonify({'error': ve.errors() }), 400
    
    # replace values of 7-12 digits with *
    numero = data.numero_tarjeta
    data.numero_tarjeta = numero[:6] + 'X' * 6 + numero[-4:]
    
    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_metodo_pago", [data.nombre, data.numero_tarjeta, client["id_cliente"], 0, 0, ''])
        cursor.execute("SELECT @_sp_register_metodo_pago_4 AS rows_affected, @_sp_register_metodo_pago_5 AS last_id, @_sp_register_metodo_pago_6 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo registrar el método de pago. {e}'}), 500
    finally:
      db.close()

    if result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({ 'message': 'Método de pago registrado' }), 201