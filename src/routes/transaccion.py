from flask import Blueprint

from controllers.transaccion import TransaccionController

transaccion_router = Blueprint('transaccion', __name__)

@transaccion_router.route('/client/transactions', methods=['GET'])
def get_all_transactions_by_id_client():
  """
  Obtener todas las transacciones del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Transacciones del cliente
      schema:
        type: array
        items:
          type: object
          properties:
            id_transaccion:
              type: integer
              example: 1
            fecha_compra:
              type: string
              example: "2000-01-01"
            hora_compra:
              type: string
              example: "00:00:00"
            precio_total:
              type: float
              example: 100
  """
  return TransaccionController.get_all_transactions_by_id_client()

@transaccion_router.route('/transaction/pdf/<int:id_transaccion>/generate', methods=['GET'])
def create_pdf_transaction(id_transaccion):
  """
  Generar el PDF de la transaccion
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_transaccion
      required: true
      schema:
        type: integer
        example: 1
  responses:
    200:
      description: PDF de la transaccion
    404:
      description: No se ha encontrado el id seleccionado
  """
  return TransaccionController.create_pdf_transaction(id_transaccion)

@transaccion_router.route('/transaction/pdf/<string:name>', methods=['GET'])
def get_pdf_transaction(name):
  """
  Redirecciona al recurso PDF
  ---
  parameters:
    - in: path
      name: name
      required: true
      schema:
        type: string
        example: "hash"
  """
  return TransaccionController.get_pdf_transaction(name)

@transaccion_router.route('/transaction/new', methods=['POST'])
def post_new_transaction_with_tickets():
  """
  Generar una nueva transaccion con tickets
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
          precio_neto:
            type: float
            example: 100.00
          igv:
            type: float
            example: 18.00
          precio_total:
            type: float
            example: 118.00
          fecha_compra:
            type: string
            example: "2000-01-01 10:00:00"
          ruc:
            type: string
            example: "1234567890"
          correo_contacto:
            type: string
            example: "correo@correo.com"
          telefono_contacto:
            type: string
            example: "123456789"
          id_cliente:
            type: integer
            example: 1
          id_descuento:
            type: integer
            example: 1
          id_tipo_boleta:
            type: integer
            example: 1
          id_metodo_pago:
            type: integer
            example: 1
          pasajes:
            type: array
            items:
              type: object
              properties:
                precio_neto:
                  type: float
                  example: 100.00
                igv:
                  type: float
                  example: 18.00
                precio_total:
                  type: float
                  example: 118.00
                id_pasajero:
                  type: integer
                  example: 1
                id_asiento:
                  type: integer
                  example: 1
                id_viaje_programado:
                  type: integer
                  example: 1
  responses:
    200:
      description: Transaccion creada
    400:
      description: Error al crear la transaccion
  """
  return TransaccionController.post_new_transaction_with_tickets()