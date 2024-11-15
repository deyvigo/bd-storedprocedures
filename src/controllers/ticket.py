from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError

from services.database import Database

class TicketController:
  @staticmethod
  @jwt_required()
  def get_all_tickets_by_id_client():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_pasaje_by_id_cliente', [client['id_cliente']])
        response = cursor.fetchall()
    except Exception as e:
      return { 'error': f'No se pudo obtener los boletos del cliente. {e}' }, 400
    finally:
      db.close()
    
    if not response:
      return { 'error': 'No tienes boletos' }, 404
    
    for r in response:
      r['hora_salida'] = str(r['hora_salida'])
    
    return jsonify(response), 200
