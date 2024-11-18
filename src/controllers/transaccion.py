from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.database import Database

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