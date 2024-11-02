from flask import request, jsonify
from pydantic import ValidationError
from flask_bcrypt import Bcrypt
from psycopg2.extras import RealDictCursor

from dto.signupDTO import AdminSignUpDTO, ClientSignUpDTO
from services.database import Database

bcrypt = Bcrypt()

class SignUpController:
  @staticmethod
  def signup_admin():
    try:
      data = AdminSignUpDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    db = Database().connection()

    hashed_password = bcrypt.generate_password_hash(data.password).decode('utf-8')

    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc('get_admin_by_username', [data.username])
        admin_on_db = cursor.fetchone()

        if admin_on_db:
          return jsonify({ 'error': 'El usuario ya existe' }), 400

        args = [
          data.nombre,
          data.apellido_pat,
          data.apellido_mat,
          data.fecha_nacimiento.strftime('%Y-%m-%d'),
          data.dni,
          data.sexo,
          data.telefono,
          data.correo,
          data.username,
          hashed_password,
          0,
          0,
          ''
        ]

        cursor.execute("CALL sp_register_admin(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", args)
        result = cursor.fetchone()

        if result and result["error_message"]:
          db.rollback()
          return jsonify({ 'error': result["error_message"] }), 409
        
        last_id, rows_affected = result["last_id"], result["rows_affected"]
        
        if rows_affected <= 0:
          db.rollback()
          return jsonify({ 'error': 'No se pudo registrar al admin' }), 400

        db.commit()
        return jsonify({
          'message': 'Admin registrado exitosamente',
          'rows_affected': rows_affected,
          'last_id': last_id
        }), 201
    except Exception as e:
      db.rollback()
      return jsonify({'error': f'No se pudo registrar al admin. {e}'}), 500
    finally:
      db.close()

  @staticmethod
  def signup_client():
    try:
      data = ClientSignUpDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    db = Database().connection()

    hashed_password = bcrypt.generate_password_hash(data.password).decode('utf-8')
    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.callproc('get_cliente_by_username', [data.username])
        cliente_on_db = cursor.fetchone()

        if cliente_on_db:
          return jsonify({ 'error': 'El usuario ya existe' }), 400
        
        args = [
          data.nombre,
          data.apellido_pat,
          data.apellido_mat,
          data.fecha_nacimiento.strftime('%Y-%m-%d'),
          data.dni,
          data.sexo,
          data.telefono,
          data.correo,
          data.username,
          hashed_password,
          0,
          0,
          ''
        ]
        cursor.execute("CALL sp_register_cliente(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", args)
        result = cursor.fetchone()

        if result and result["error_message"]:
          db.rollback()
          return { "error": result["error_message"] }, 409
        
        last_id, rows_affected = result["last_id"], result["rows_affected"]

        if rows_affected <= 0:
          db.rollback()
          return jsonify({ 'error': 'No se pudo registrar al cliente' }), 400

        db.commit()
        return jsonify({
          'message': 'Cliente registrado exitosamente',
          'rows_affected': rows_affected,
          'last_id': last_id
        }), 201
    except Exception as e:
      db.rollback()
      return jsonify({'error': f'No se pudo registrar el cliente. {e}'}), 500
    finally:
      db.close()

