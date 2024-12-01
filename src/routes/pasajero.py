from flask import Blueprint

from controllers.pasajero import PasajeroController

pasajero_router = Blueprint('pasajero', __name__)

@pasajero_router.route('/pasajero', methods=['POST'])
def create_pasajero():
  """
  Crear un pasajero
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          dni:
            type: string
            example: "12345678"
          nombre:
            type: string
            example: "Juan"
          apellido_pat:
            type: string
            example: "Perez"
          apellido_mat:
            type: string
            example: "Perez"
          fecha_nacimiento:
            type: string
            format: date
            example: "1990-01-01"
          sexo:
            type: string
            example: "masculino"
  responses:
    201:
      description: Pasajero creado
    400:
      description: Error al crear el pasajero
  """
  return PasajeroController.create_pasajero()
