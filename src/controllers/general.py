from flask import request, jsonify
from flask_jwt_extended import jwt_required

from services.database import Database
import datetime
import decimal

class ControllerGeneral:
  
  @staticmethod
  def get_origins_available():
    db = Database().connection()
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_origins_available', [])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f'No se pudo obtener la información de las ciudades. {e}'}), 500
    finally:
      db.close()
      
    if not response:
      return jsonify({ 'error': 'Ciudades no encontradas' }), 404
    
    return jsonify(response), 200
  
  @staticmethod
  def get_destination_by_city():
    db = Database().connection()
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_destinos_by_city', [request.json['ciudad_origen']])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f'No se pudo obtener la información de la ciudad. {e}'}), 500
    finally:
      db.close()
      
    if not response:
      return jsonify({ 'error': 'Ciudad no encontrada' }), 404
    
    return jsonify(response), 200
  
  @staticmethod
  @jwt_required()
  def get_seat_by_trip():
    db = Database().connection()
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_seat_by_trip', [request.json['id_viaje_programado']])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f'No se pudo obtener la información del viaje. {e}'}), 500
    finally:
      db.close()

    if not response:
        return jsonify({ 'error': 'Viaje no encontrado' }), 404
    
    return jsonify(response), 200
    
  @staticmethod
  def get_scheduled_trip():
    db = Database().connection()
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_scheduled_trip',[request.json['ciudad_origen'], request.json['ciudad_destino'],request.json['fecha']])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f"No se pudo obtener la información de los viajes programados en la ruta {request.json['ciudad_origen']} a {request.json['ciudad_destino']} en fecha {request.json['fecha']}. {e}"}), 500
    finally:
      db.close()
    print(response)
    for row in response:
      if isinstance(row['fecha_salida'], datetime.date):
          row['fecha_salida'] = row['fecha_salida'].strftime('%Y-%m-%d')  
      
      if isinstance(row['duracion'], datetime.timedelta):
          row['duracion'] = str(row['duracion']) 
      
      if isinstance(row['hora_llegada'], int):
          hours = row['hora_llegada'] // 3600
          minutes = (row['hora_llegada'] % 3600) // 60
          seconds = row['hora_llegada'] % 60
          row['hora_llegada'] = f'{hours:02}:{minutes:02}:{seconds:02}'

      if isinstance(row['hora_salida'], datetime.timedelta):
          total_seconds = row['hora_salida'].total_seconds()
          hours = total_seconds // 3600
          minutes = (total_seconds % 3600) // 60
          seconds = total_seconds % 60
          row['hora_salida'] = f'{int(hours):02}:{int(minutes):02}:{int(seconds):02}'

      if isinstance(row['precio_min'], decimal.Decimal):
          row['precio_min'] = float(row['precio_min'])  
    if not response:
      return jsonify({ 'error': 'Viajes programados no encontrados' }), 404
      
    return jsonify(response), 200    
