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
        # check if the username already exists
        cursor.callproc('check_admin_username_exists', (data.username, 0))
        cursor.execute('SELECT @_check_admin_username_exists_1 AS exists_flag;')
        exists_flag = cursor.fetchone()['exists_flag']

        if exists_flag:
          return jsonify({ 'error': 'El usuario ya existe' }), 400

        # then register the admin
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
          0
        ]
        cursor.callproc('post_admin', args)
        cursor.execute('SELECT @_post_admin_10 AS rows_affected, @_post_admin_11 AS last_id;')
        result = cursor.fetchone()
        rows_affected = result['rows_affected']
        last_id = result['last_id']
        db.commit()

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
        # check if the username already exists
        cursor.callproc('check_cliente_username_exists', (data.username, 0))
        cursor.execute('SELECT @_check_cliente_username_exists_1 AS exists_flag;')
        exists_flag = cursor.fetchone()['exists_flag']

        if exists_flag:
          return jsonify({ 'error': 'El usuario ya existe' }), 400

        # then register the client
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
          0
        ]
        cursor.callproc('post_cliente', args)
        cursor.execute('SELECT @_post_cliente_10 AS rows_affected, @_post_cliente_11 AS last_id;')
        result = cursor.fetchone()
        rows_affected = result['rows_affected']
        last_id = result['last_id']
        db.commit()

      return jsonify({
        'message': 'Cliente registrado exitosamente',
        'rows_affected': rows_affected,
        'last_id': last_id
      }), 201
    except Exception as e:
      db.rollback()
      return jsonify({'error': f'No se pudo registrar el cliente. {e}'}), 500

