from flask import Blueprint

from controllers.login import LoginController

login = Blueprint('login', __name__)

@login.route('/login/admin', methods=['POST'])
def login_admin():
  """
  Login del admin para obtener un JWT
  ---
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: string
        properties:
          username:
            type: string
            example: "admin"
            description: Usuario del cliente
          password:
            type: string
            example: "12345678"
            description: Contraseña del cliente
  responses:
    200:
      description: Login exitoso
      content:
        application/json:
          example:
            jwt_token: "JWT_TOKEN"
            message: "Login exitoso"
    401:
      description: Credenciales incorrectas
  """
  return LoginController.login_admin()

@login.route('/login/client', methods=['POST'])
def login_client():
  """
  Login del cliente para obtener un JWT
  ---
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: string
        properties:
          username:
            type: string
            example: "cliente1"
            description: Usuario del cliente
          password:
            type: string
            example: "12345678"
            description: Contraseña del cliente
  responses:
    200:
      description: Login exitoso
      content:
        application/json:
          example:
            jwt_token: "JWT_TOKEN"
            message: "Login exitoso"
    401:
      description: Credenciales incorrectas
  """
  return LoginController.login_client()