from flask import request, jsonify
from flask_jwt_extended import jwt_required
from psycopg2.extras import RealDictCursor

from services.database import Database


class ChoferController:
  @staticmethod
  @jwt_required()
  def get_all_choferes():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM fn_get_choferes()')
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se encontraron choferes' }), 404
    return jsonify(response), 200

  
  @staticmethod
  @jwt_required()
  def register_chofer():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        data = request.json
        i_nombre = data["nombre"]
        i_apellido_pat = data["apellido_pat"]
        i_apellido_mat = data["apellido_mat"]
        i_dni = data["dni"]
        i_sexo = data["sexo"]
        cursor.execute('SELECT * FROM fn_register_chofer(%s, %s, %s, %s, %s,0,0,"")', (i_nombre, i_apellido_pat, i_apellido_mat, i_dni, i_sexo))
        response = cursor.fetchone()    
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se pudo registrar el chofer' }), 404
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def update_chofer():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        data = request.json
        i_id_chofer = data["id_chofer"]
        i_nombre = data["nombre"]
        i_apellido_pat = data["apellido_pat"]
        i_apellido_mat = data["apellido_mat"]
        i_dni = data["dni"]
        i_sexo = data["sexo"]
        cursor.execute('SELECT * FROM fn_update_chofer(%s, %s, %s, %s, %s, %s)', (i_id_chofer, i_nombre, i_apellido_pat, i_apellido_mat, i_dni, i_sexo))
        response = cursor.fetchone()    
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se pudo registrar el chofer' }), 404
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def update_status_chofer_by_id():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        data = request.json
        i_id_chofer = data["id_chofer"]
        cursor.execute('SELECT * FROM sp_update_status_chofer_by_id(%s)', (i_id_chofer,))
        response = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se pudo registrar el chofer' }), 404
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def get_hired_choferes():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM vw_hired_chofer;')
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se encontraron choferes contratados' }), 404
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def get_fired_choferes():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM vw_fired_chofer;')
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se encontraron choferes contratados' }), 404
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def get_free_chofer():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        data = request.json
        i_date = data["date"]
        cursor.execute('SELECT * FROM sp_get_free_chofer(%s) ', (i_date,))
        response = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se encontraron choferes libres' }), 404
    return jsonify(response), 200