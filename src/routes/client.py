from flask import Blueprint

from controllers.client import ClientController

client_router = Blueprint('client', __name__)

@client_router.route('/client/info', methods=['GET'])
def get_all_client_info():
  """
  Obtener información del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Información del cliente
      schema:
        type: object
        properties:
          apellido_pat:
            type: string
            example: "Apellido Paterno"
          apellido_mat:
            type: string
            example: "Apellido Materno"
          correo:
            type: string
            example: "correo@correo.com"
          dni:
            type: string
            example: "12345678"
          fecha_nacimiento:
            type: string
            example: "2000-01-01"
          id_cliente:
            type: integer
            example: 1
          nombre:
            type: string
            example: "Nombre"
          sexo:
            type: string
          telefono:
            type: string
            example: "123456789"
          username:
            type: string
            example: "username"
    401:
      description: No autorizado
  """
  return ClientController.get_all_client_info()

@client_router.route('/client/payment-methods', methods=['GET'])
def get_all_client_payment_methods():
  """
  Obtener los métodos de pago del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Métodos de pago del cliente
      schema:
        type: array
        items:
          type: object
          properties:
            id_metodo_pago:
              type: integer
              example: 1
            estado:
              type: enum
              values:
                - activo
                - inactivo
              example: "activo"
            nombre:
              type: string
              example: "Tarjeta 1"
            numero_tarjeta:
              type: string
              example: "123456XXXXXX3456"
            id_cliente:
              type: integer
              example: 1
    404:
      description: No tienes métodos de pago
  """
  return ClientController.get_all_client_payment_methods()

@client_router.route('/client/payment-method/<int:id_metodo_pago>', methods=['PATCH'])
def delete_client_payment_method(id_metodo_pago):
  """
  Eliminar un método de pago del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_metodo_pago
      required: true
      schema:
        type: integer
        example: 1
  responses:
    200:
      description: Método de pago eliminado
      content:
        application/json:
          example:
            message: "Método de pago eliminado"
    400:
      description: Error al eliminar el método de pago
  """
  return ClientController.delete_client_payment_method(id_metodo_pago)

@client_router.route('/client/payment-method', methods=['POST'])
def create_client_payment_method():
  """
  Crear un método de pago del cliente
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
          nombre:
            type: string
            example: "Tarjeta 1"
          numero_tarjeta:
            type: string
            example: "123456XXXXXX3456"
  responses:
    201:
      description: Método de pago registrado
  """
  return ClientController.create_client_payment_method()

@client_router.route('/client/payment-method/<int:id_metodo_pago>', methods=['PUT'])
def update_client_payment_method(id_metodo_pago):
  """
  Actualizar un método de pago del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_metodo_pago
      required: true
      schema:
        type: integer
        example: 1
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          nombre:
            type: string
            example: "Tarjeta 1"
          numero_tarjeta:
            type: string
            example: "123456XXXXXX3456"
  responses:
    200:
      description: Método de pago actualizado
  """
  return ClientController.update_client_payment_method(id_metodo_pago)