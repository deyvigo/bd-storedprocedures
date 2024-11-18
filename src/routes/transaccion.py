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