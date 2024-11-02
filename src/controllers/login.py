from flask import request, jsonify
from pydantic import ValidationError
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from datetime import timedelta
from psycopg2.extras import RealDictCursor

from dto.loginDTO import AdminLoginDTO, ClientLoginDTO
from dto.adminDTO import AdminDTO
from dto.clienteDTO import ClienteDTO
from services.database import Database

bcrypt = Bcrypt()

class LoginController:
  @staticmethod
  def login_admin():
    try:
      data = AdminLoginDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    db = Database().connection()

    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        args = [data.username]
        cursor.callproc('get_admin_by_username', args)
        response = cursor.fetchone()

        if not response:
          return jsonify({ 'error': 'El usuario no existe' }), 400

        try:
          admin_in_db = AdminDTO(**response)
        except ValidationError as ve:
          return jsonify({ 'error': 'La base de datos no ha obtenido los datos necesarios' }), 400

        if not bcrypt.check_password_hash(admin_in_db.password, data.password):
          return jsonify({ 'error': 'La contraseña es incorrecta' }), 400
      
      # return jwt
      token = create_access_token(identity={
        'id_admin': admin_in_db.id_admin,
        'username': admin_in_db.username,
        'fullname': f'{admin_in_db.nombre} {admin_in_db.apellido_pat} {admin_in_db.apellido_mat}'
      }, expires_delta=timedelta(days=7))

      return jsonify({ "message": "Login exitoso", "jwt_token": token }), 200
    except Exception as e:
      return jsonify({'error': f'No se pudo realizar el login. {e}'}), 500

  @staticmethod
  def login_client():
    try:
      data = ClientLoginDTO(**request.json)
    except ValidationError as ve:
      return jsonify({ 'error': ve.errors() }), 400

    db = Database().connection()

    try:
      with db.cursor(cursor_factory=RealDictCursor) as cursor:
        args = [data.username]
        cursor.callproc('get_cliente_by_username', args)
        response = cursor.fetchone()

        if not response:
          return jsonify({ 'error': 'El usuario no existe' }), 400
        
        try:
          cliente_in_db = ClienteDTO(**response)
        except ValidationError as ve:
          return jsonify({ 'error': 'La base de datos no ha obtenido los datos necesarios' }), 400
        
        if not bcrypt.check_password_hash(cliente_in_db.password, data.password):
          return jsonify({ 'error': 'La contraseña es incorrecta' }), 400

      # return jwt
      token = create_access_token(identity={
        'id_cliente': cliente_in_db.id_cliente,
        'username': cliente_in_db.username,
        'fullname': f'{cliente_in_db.nombre} {cliente_in_db.apellido_pat} {cliente_in_db.apellido_mat}'
      }, expires_delta=timedelta(days=7))

      return jsonify({ "message": "Login exitoso", "jwt_token": token }), 200
    except Exception as e:
      return jsonify({'error': f'No se pudo realizar el login. {e}'}), 500

      