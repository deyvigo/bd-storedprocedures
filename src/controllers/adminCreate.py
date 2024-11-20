from flask import request, jsonify
from flask_jwt_extended import jwt_required , get_jwt_identity
from pydantic import ValidationError
from services.database import Database
from dto.adminCreateDTO import BusCreateDTO , AsientoDTO , RutaDTO ,TerminalCreateDTO , ParadaDTO
class AdminController:
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

  @staticmethod
  @jwt_required()
  def admin_create_bus():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      data =BusCreateDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_bus", [data.asientos, data.placa, data.marca, data.niveles,request.json["id_tipo_servicio_bus"],0,0,""])
        cursor.execute("SELECT @_sp_register_bus_4 AS last_id,@_sp_register_bus_6 AS rows_affected,@_sp_register_bus_7 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo registrar el bus. {e}'}), 500
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({
      'message': 'Bus creado exitosamente',
      'id_bus': result['last_id'],
      'asientos': data.asientos,
      'placa': data.placa,
      'marca': data.marca,
      'niveles': data.niveles,
      'id_tipo_servicio_bus': request.json["id_tipo_servicio_bus"]
    }), 201
  
  @staticmethod
  @jwt_required()
  def admin_create_asiento():
    admin = get_jwt_identity()
    db=Database().connection()

    try:
      data=AsientoDTO(**request.json)
    except ValidationError as ve:
      return jsonify({'error': ve.errors()}),400

    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_asiento",[data.nivel,data.numero,request.json["id_bus"],0,0,''])
        cursor.execute("SELECT @_sp_register_asiento_3 AS last_id,@_sp_register_asiento_4 AS rows_affected,@_sp_register_asiento_5 AS error_message;")
        result=cursor.fetchone()
    except Exception as e:
      return jsonify({'error': f'No se pudo registrar el asiento. {e}'}),500
    finally:
      db.close()

    if result and result['error_message']:
      return jsonify({'error': result['error_message']}),400

    return jsonify({
      'message':'Asiento creado exitosamente',
      'id_asiento':result['last_id'],
      'nivel':data.nivel,
      'numero':data.numero,
      'id_bus':request.json["id_bus"]
    }),201  

  @staticmethod
  @jwt_required()
  def admin_create_route():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      data = RutaDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400
    
    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_ruta", [data.duracion_estimada.strftime('%H:%M:%S'), data.distancia, data.estado, data.id_origen,data.id_destino, 0, 0, ''])
        cursor.execute("SELECT @_sp_register_ruta_5 AS last_id,@_sp_register_ruta_6 AS rows_affected,@_sp_register_ruta_7 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo registrar la ruta. {e}'}), 500
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({
      'message': 'Ruta creada exitosamente',
      'id_ruta': result['last_id'],
      'duracion_estimada': data.duracion_estimada.strftime('%H:%M:%S'),
      'distancia': data.distancia,
      'estado': data.estado,
      'id_origen': data.id_origen ,
      'id_destino': data.id_destino
    }), 201
  
  @staticmethod
  @jwt_required()
  def admin_create_parada():
    admin = get_jwt_identity()
    db = Database().connection()

    try:
      data = ParadaDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400
    
    try:
      with db.cursor() as cursor:
        cursor.callproc("sp_register_parada_intermedia", [data.ordinal, data.id_terminal, request.json["id_ruta"], 0, 0, ''])
        cursor.execute("SELECT @_sp_register_parada__intermedia_3 AS last_id,@_sp_register_parada_intermedia_4 AS rows_affected,@_sp_register_parada_intermedia_5 AS error_message;")
        result = cursor.fetchone()
    except Exception as e:
      return jsonify({ 'error': f'No se pudo registrar la parada. {e}'}), 500
    finally:
      db.close()
    
    if result and result['error_message']:
      return jsonify({ 'error': result['error_message'] }), 400
    
    return jsonify({
      'message': 'Parada creada exitosamente',
      'id_parada_intermedia': result['last_id'],
      'ordinal': data.ordinal,
      'id_terminal': data.id_terminal,
      'id_ruta': request.json["id_ruta"],
    }), 201