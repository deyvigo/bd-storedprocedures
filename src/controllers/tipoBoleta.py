from flask import jsonify
from services.database import Database


class TipoBoletaController:
  @staticmethod 
  def get_tipo_boleta_by_tipo(tipo):
    db = Database().connection()

    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_tipo_boleta_by_tipo', [tipo])
        response = cursor.fetchone()
    except Exception as e:
      return {'error': f'No se puede recuperar los datos: {e}'}, 400
    finally:
      db.close()

    if not response:
      return {'error': 'No se encontraron datos'}, 404

    return jsonify(response), 200
