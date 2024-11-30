from flask import request, jsonify
from flask_jwt_extended import jwt_required

from psycopg2.extras import RealDictCursor

from services.database import Database  
import decimal
import datetime
class ControllerGeneral:
  
  @staticmethod
  @jwt_required()
  def get_origins_available():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM vw_get_origins_available')
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    
    if not response:
      return jsonify({ 'error': 'No se encontraron ciudades disponibles' }), 404             
    return jsonify(response), 200
    
  @staticmethod
  @jwt_required()
  def get_destinations_available():
    db = Database().connection()
    try:
      data = request.json
      i_departamento = data["ciudad_origen"]
      print("i_departamento:",i_departamento)
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM fn_get_destinos_by_city(%s)', (i_departamento,))
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    
    if not response:
      return jsonify({ 'error': 'No se encontraron destinos disponibles' }), 404             
    return jsonify(response), 200
    
  @staticmethod
  @jwt_required()
  def get_cities_available():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM vw_get_cities_available')
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    
    if not response:
      return jsonify({ 'error': 'No se encontraron ciudades disponibles' }), 404             
    return jsonify(response), 200
    
  @staticmethod
  @jwt_required()
  def get_scheduled_trip():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        data = request.json
        i_destino = data["ciudad_destino"]
        i_origen = data["ciudad_origen"]
        i_fecha = data["fecha"]
        cursor.execute('SELECT * FROM fn_get_scheduled_trip(%s, %s, %s)', (i_origen, i_destino, i_fecha))
        response = cursor.fetchall()
        print(response)
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400 
    
    if not response:
      return jsonify({ 'error': 'No se encontraron viajes programados' }), 404
    for row in response:
      if row['hora_salida']:
          row['hora_salida'] = row['hora_salida'].strftime('%H:%M:%S')
      if row['hora_llegada']:
          row['hora_llegada'] = row['hora_llegada'].strftime('%H:%M:%S')   
      if row['duracion']:
          row['duracion'] = row['duracion'].strftime('%H:%M:%S')  # Si es time, convertir a string
      if isinstance(row['precio_min'], decimal.Decimal):
          row['precio_min'] = float(row['precio_min'])  # Convertir Decimal a float
      if isinstance(row['fecha_salida'], datetime.date):
          row['fecha_salida'] = row['fecha_salida'].strftime('%Y-%m-%d')  # Convertir date a string 
    print(response)         
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def get_seats_by_trip():
    db = Database().connection()
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        data = request.json
        i_id_viaje_programado = data["id_viaje_programado"]
        print("i_id_viaje_programado:",i_id_viaje_programado)
        cursor.execute('SELECT * FROM fn_get_seat_by_trip(%s)', (i_id_viaje_programado,))
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({ 'error': f'La base de datos no ha obtenido los datos necesarios {e}' }), 400
    if not response:
      return jsonify({ 'error': 'No se encontraron asientos' }), 404             
    return jsonify(response), 200