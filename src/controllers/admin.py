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
  # def admin_create_bus():
    # admin = get_jwt_identity()
    # db = Database().connection()

    # ##autenticamos (dto de bus)?
    # try:
    #   with db.cursor() as cursor:
    #     cursor.callproc("sp_register_bus", [asientos,placa,marca,niveles,tipo_servicio_bus["id_tipo_servicio_bus"],0,0,""])
    #     cursor.execute("SELECT @_sp_register_bus_5 AS last_id,@_sp_register_bus_6 AS rows_affected,@_sp_register_bus_7 AS error_message;")
    #     result = cursor.fetchone()
    # except Exception as e:
    #   return jsonify({'error': f'No se pudo registrar el bus. {e}'}), 500
    # finally:
    #   db.close()
    
    # if result and result['error_message']:
    #   return jsonify({ 'error': result['error_message'] }), 400
    
    # return jsonify({
    #   'message': 'Bus creado exitosamente',
    #   'id_bus': result['last_id'],
    #   'asientos': asientos,
    #   'placa': placa,
    #   'marca': marca,
    #   'niveles': niveles,
    #   'tipo_servicio_bus': tipo_servicio_bus
    # }), 201
  
  def admin_create_bus():
        admin = get_jwt_identity()  # Identidad del administrador que hace la solicitud
        db = Database().connection()

        # Extraer datos enviados desde el cuerpo de la solicitud
        try:
            data = request.get_json()  # Obtiene el cuerpo de la solicitud como un diccionario
            asientos = data.get("asientos")
            placa = data.get("placa")
            marca = data.get("marca")
            niveles = data.get("niveles")
            id_tipo_servicio_bus = data.get("id_tipo_servicio_bus")

            # Validar que todos los campos requeridos están presentes
            if not all([asientos, placa, marca, niveles, id_tipo_servicio_bus]):
                return jsonify({"error": "Faltan datos obligatorios para registrar el bus."}), 400

            # Llamada al procedimiento almacenado
            with db.cursor() as cursor:
                cursor.callproc("sp_register_bus", [
                    asientos,
                    placa,
                    marca,
                    niveles,
                    id_tipo_servicio_bus,  # Usamos el valor enviado
                    0,
                    0,
                    ""
                ])
                cursor.execute("""
                    SELECT 
                        @_sp_register_bus_5 AS last_id, 
                        @_sp_register_bus_6 AS rows_affected, 
                        @_sp_register_bus_7 AS error_message;
                """)
                result = cursor.fetchone()

        except Exception as e:
            return jsonify({'error': f'No se pudo registrar el bus. {e}'}), 500

        finally:
            db.close()

        # Verificar si hubo un error desde el procedimiento almacenado
        if result and result["error_message"]:
            return jsonify({"error": result["error_message"]}), 400

        # Respuesta exitosa
        return jsonify({
            "message": "Bus creado exitosamente",
            "id_bus": result["last_id"],
            "asientos": asientos,
            "placa": placa,
            "marca": marca,
            "niveles": niveles,
            "id_tipo_servicio_bus": id_tipo_servicio_bus
        }), 201