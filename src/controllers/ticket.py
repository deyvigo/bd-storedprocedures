from flask import jsonify, send_file, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from psycopg2.extras import RealDictCursor

from services.database import Database
from services.createTicketPDF import draw_ticket_pdf

class TicketController:
  @staticmethod
  @jwt_required()
  def get_all_tickets_by_id_client():
    client = get_jwt_identity()
    db = Database().connection()

    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc('fn_get_pasaje_by_id_cliente', [client['id_cliente']])
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
  def create_pdf_ticket(id_pasaje):
    db = Database().connection()

    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc('fn_get_pasaje_by_id_pasaje_for_pdf', [id_pasaje])
        response = cursor.fetchone()
    except Exception as e:
      return { 'error': f'No se pudo obtener el PDF del boleto. {e}' }, 400
    finally:
      db.close()

    try:
      ticket_name =draw_ticket_pdf(response)
    except Exception as e:
      return { 'error': f'No se pudo generar el PDF del boleto. {e}' }, 400
    
    return { 'message': 'PDF generado', 'ticket_name': ticket_name }, 200
  
  @staticmethod
  def get_pdf_ticket(name):
    try:
      path = os.path.join(os.getcwd(), f'tickets/{name}.pdf')
      if not os.path.exists(path):
        abort(404, description='No se ha encontrado el recurso')

      return send_file(path)
    except FileNotFoundError:
      abort(404, description='No se ha encontrado el recurso')