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