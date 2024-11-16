from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.database import Database
from services.createTicketPDF import draw_ticket_pdf

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
  
  @staticmethod
  @jwt_required()
  def get_pdf_ticket(id_pasaje):
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_print_pasaje_by_id_pasaje', [id_pasaje])
        response = cursor.fetchone()
    except Exception as e:
      return { 'error': f'No se pudo obtener el PDF del boleto. {e}' }, 400
    finally:
      db.close()

    print(response)
    draw_ticket_pdf(response)

    return { 'message': 'PDF generado' }, 200

