from flask import request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from pydantic import ValidationError
from services.database import Database
from dto.TerminalDTO import TerminalCreateDTO

class AdminController:
  @staticmethod
  @jwt_required()
  def create_admin_terminal():
    admin = get_jwt_identity()
    db = Database().connection()

  # falta importar y crear la clase TerminalCreateDTO
    try:
      data= TerminalCreateDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400
    
    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_terminal", [data.nombre, data.departamento, data.provincia,0,0,''])
        cursor.execute("SELECT @_sp_register_terminal_3 AS last_id,@_sp_register_terminal_4 AS rows_affected,@_sp_register_terminal_5 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo registrar la terminal. {e}'}), 500
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({
      'message': 'Terminal creada exitosamente',
      'id_terminal': result['last_id'],
      'nombre': data.nombre,
      'departamento': data.departamento,
      'provincia': data.provincia
    }), 201