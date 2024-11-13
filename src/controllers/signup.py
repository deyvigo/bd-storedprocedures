from flask import request, jsonify
from pydantic import ValidationError
from flask_bcrypt import Bcrypt

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
      with db.cursor() as cursor:
        args = [
          data.nombre,
          data.apellido_pat,
          data.apellido_mat,
          data.fecha_nacimiento.strftime('%Y-%m-%d'),
          data.dni,
          str(data.sexo).lower(),
          data.telefono,
          data.correo,
          data.username,
          hashed_password,
          0,
          0,
          ''
        ]
        cursor.callproc('sp_register_admin', args)
        cursor.execute('SELECT @_sp_register_admin_10 AS rows_affected, @_sp_register_admin_11 AS last_id, @_sp_register_admin_12 AS error_message;')
        result = cursor.fetchone()
        rows_affected = result['rows_affected']
        last_id = result['last_id']
        error_message = result['error_message']
        
        if error_message:
          return jsonify({ 'error': error_message }), 400

        return jsonify({
          'message': 'Admin registrado exitosamente',
          'rows_affected': rows_affected,
          'last_id': last_id
        }), 201
    except Exception as e:
      db.rollback()
      return jsonify({'error': f'No se pudo registrar el admin. {e}'}), 500

  @staticmethod
  def signup_client():
    try:
      data = ClientSignUpDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    db = Database().connection()

    hashed_password = bcrypt.generate_password_hash(data.password).decode('utf-8')
    try:
      with db.cursor() as cursor:
        args = [
          data.nombre,
          data.apellido_pat,
          data.apellido_mat,
          data.fecha_nacimiento.strftime('%Y-%m-%d'),
          data.dni,
          str(data.sexo).lower(),
          data.telefono,
          data.correo,
          data.username,
          hashed_password,
          0,
          0,
          ''
        ]
        cursor.callproc('sp_register_cliente', args)
        cursor.execute('SELECT @_sp_register_cliente_10 AS rows_affected, @_sp_register_cliente_11 AS last_id, @_sp_register_cliente_12 AS error_message;')
        result = cursor.fetchone()
        rows_affected = result['rows_affected']
        last_id = result['last_id']
        error_message = result['error_message']

        if error_message:
          return jsonify({ 'error': error_message }), 400

        return jsonify({
          'message': 'Cliente registrado exitosamente',
          'rows_affected': rows_affected,
          'last_id': last_id
        }), 201
    except Exception as e:
      db.rollback()
      return jsonify({'error': f'No se pudo registrar el cliente. {e}'}), 500

