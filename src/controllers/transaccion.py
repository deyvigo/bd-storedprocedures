from flask import jsonify, abort, send_file,request
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import json

from services.database import Database
from services.createTransaccionPDF import draw_transaccion_pdf

class TransaccionController:
  @staticmethod
  @jwt_required()
  def get_all_transactions_by_id_client():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_transaccion_by_id_cliente', [client['id_cliente']])
        response = cursor.fetchall()
    except Exception as e:
      print(e)
      return { 'error': f'No se pudo obtener las transacciones del cliente.' }, 400
    
    if not response:
      return { 'error': 'No tienes transacciones' }, 404
    
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def create_pdf_transaction(id_transaccion):
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_transaccion_by_id', [id_transaccion])
        response = cursor.fetchone()
    except Exception as e:
      return { 'error': f'No se pudo obtener la transaccion del id seleccionado. {e}' }, 400
    finally:
      db.close()

    try:
      transaction_name =draw_transaccion_pdf(response)
    except Exception as e:
      return { 'error': f'No se pudo generar el PDF de la transaccion. {e}' }, 400
    
    return { 'message': 'PDF generado', 'transaction_name': transaction_name }, 200
  
  @staticmethod
  def get_pdf_transaction(name):
    try:
      path = os.path.join(os.getcwd(), f'transactions/{name}.pdf')
      if not os.path.exists(path):
        abort(404, description='No se ha encontrado el recurso')

      return send_file(path)
    except FileNotFoundError:
      abort(404, description='No se ha encontrado el recurso')
      
  @staticmethod
  @jwt_required()
  def post_new_transaction_with_tickets():
    db = Database().connection()
    try:
      data = request.json
      precio_neto = data['precio_neto']
      igv = data['igv']
      precio_total = data['precio_total']
      fecha_compra = data['fecha_compra']
      ruc = data['ruc']
      correo_contacto = data['correo_contacto']
      telefono_contacto = data['telefono_contacto']
      id_cliente = data['id_cliente']
      id_descuento = data['id_descuento']
      id_tipo_boleta = data['id_tipo_boleta']
      id_metodo_pago = data['id_metodo_pago']
      pasajes =json.dumps(data['pasajes'])
      args = [precio_neto, igv, precio_total, fecha_compra, ruc, correo_contacto, telefono_contacto, id_cliente, id_descuento, id_tipo_boleta, id_metodo_pago, pasajes,""]
      with db.cursor() as cursor:
        cursor.callproc('sp_register_transaction_with_tickets', args)
        cursor.execute('SELECT @_sp_register_transaction_with_tickets_12 AS error_message;')
        response = cursor.fetchone()
        error_message = response['error_message']
    except Exception as e:
      return { 'error': f'No se pudo insertar la transaccion. {e}' }, 400
    if error_message:
      return jsonify({ 'error': error_message }), 400
    return jsonify({"message":"Transaccion realizada con exito"}), 200
    
