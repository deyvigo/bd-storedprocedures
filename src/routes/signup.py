from flask import Blueprint

from controllers.signup import SignUpController

signup = Blueprint('signup', __name__)

@signup.route('/signup/admin', methods=['POST'])
def signup_admin():
  """
  Registro del admin
  ---
  parameters:
    - name: body
      in: body
      required: true
      description: Datos del admin
      schema:
        type: string
        example:
          nombre: "Nombre"
          apellido_pat: "Apellido Paterno"
          apellido_mat: "Apellido Materno"
          fecha_nacimiento: "2000-01-01"
          dni: "12345678"
          sexo: "Masculino"
          telefono: "123456789"
          correo: "correo@correo.com"
          username: "username"
          password: "12345678"
  responses:
    201:
      description: Registro exitoso
      content:
        application/json:
          example:
            message: "Admin registrado exitosamente"
            rows_affected: 1
            last_id: 1
  """
  return SignUpController.signup_admin()

@signup.route('/signup/client', methods=['POST'])
def signup_client():
  """
  Registro del cliente
  ---
  parameters:
    - name: body
      in: body
      required: true
      description: Datos del cliente
      schema:
        type: string
        example:
          nombre: "Nombre"
          apellido_pat: "Apellido Paterno"
          apellido_mat: "Apellido Materno"
          fecha_nacimiento: "2000-01-01"
          dni: "12345678"
          sexo: "Masculino"
          telefono: "123456789"
          correo: "correo@correo.com"
          username: "username"
          password: "12345678"
  responses:
    201:
      description: Registro exitoso
      content:
        application/json:
          example:
            message: "Cliente registrado exitosamente"
            rows_affected: 1
            last_id: 1 
  """
  return SignUpController.signup_client()