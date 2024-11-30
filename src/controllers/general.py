from flask import request, jsonify
from flask_jwt_extended import jwt_required

from services.database import Database

class ControllerGeneral:
  
  @staticmethod
  @jwt_required()
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
  @jwt_required()
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
  @jwt_required()
  def get_scheduled_trip():
    db = Database().connection()
    try:
      with db.cursor() as cursor:
        cursor.callproc('sp_get_scheduled_trip',[request.json['ciudad_origen'], request.json['ciudad_destino'],request.json['fecha']])
        response = cursor.fetchall()
    except Exception as e:
      return jsonify({'error': f'No se pudo obtener la información de los viajes programados en la ruta {request.json['ciudad_origen']} a {request.json['ciudad_destino']} en fecha {request.json['fecha']}. {e}'}), 500
    finally:
      db.close()

    if not response:
      return jsonify({ 'error': 'Viajes programados no encontrados' }), 404
      
    return jsonify(response), 200    