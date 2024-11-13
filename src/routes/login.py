from flask import Blueprint

from controllers.login import LoginController

login = Blueprint('login', __name__)

@login.route('/login/admin', methods=['POST'])
def login_admin():
  """
  Login del admin para obtener un JWT
  ---
  parameters:
    - name: body
      in: body
      required: true
      description: Usuario del cliente
      schema:
        type: string
        example:
          username: "admin"
          password: "12345678"
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
    - name: body
      in: body
      required: true
      description: Usuario del cliente
      schema:
        type: string
        example:
          username: "username"
          password: "12345678"
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