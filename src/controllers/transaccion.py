from flask import jsonify, abort, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from psycopg2.extras import RealDictCursor

from services.database import Database
from services.createTransaccionPDF import draw_transaccion_pdf

class TransaccionController:
  @staticmethod
  @jwt_required()
  def get_all_transactions_by_id_client():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc('fn_get_transaccion_by_id_cliente', [client['id_cliente']])
        response = cursor.fetchall()
    except Exception as e:
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
        cursor.callproc('sp_get_transaccion_by_id_for_pdf', [id_transaccion])
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
