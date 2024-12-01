from flask import jsonify
from services.database import Database


class TerminalController:
  @staticmethod
  def get_all_departamento_terminal():
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_departamento_terminal', [])
        response = cursor.fetchall()
    except Exception as e:
      return {'error': f'No se puedo recuperar los datos: {e}'}, 400
    finally:
      db.close()

    if not response:
      return {'error': 'No se encontraron datos'}, 404

    return jsonify(response), 200
