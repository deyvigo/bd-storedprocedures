from flask import request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from pydantic import ValidationError
from services.database import Database
from dto.adminCreateDTO import TerminalCreateDTO
class TerminalCreateController:
  @staticmethod
  @jwt_required()
  def get_admin_all_terminal():
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_terminal_all', [])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo recuperar los buses: {e}'}), 400
    finally:
      db.close()

    if not response:
      return jsonify({ 'error': 'No se encontraron buses'}), 404
    
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def admin_create_terminal():
    admin = get_jwt_identity()
    db = Database().connection()

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
  
  def update_terminal(id_terminal):
    db = Database().connection()
    try :
      data = TerminalCreateDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_update_terminal_by_id', [
          id_terminal,
          data.nombre,
          data.departamento,
          data.provincia,
          0,
          ''
        ])
        cursor.execute("""SELECT 
          @_sp_update_terminal_by_id_4 AS rows_affected, 
          @_sp_update_terminal_by_id_5 AS error_message;
        """)
        result = cursor.fetchone()
    except Exception as e:
        return jsonify({ 'error': f'No se pudo actualizar la terminal: {e}'}), 400
    finally:
        db.close()
    return jsonify({'message': 'Terminal actualizado'}), 200 