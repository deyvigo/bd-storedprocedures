from flask import Blueprint

from controllers.ticket import TicketController

ticket_router = Blueprint('ticket', __name__)

@ticket_router.route('/client/tickets', methods=['GET'])
def get_all_tickets():
  """
  Obtener los boletos del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Boletos del cliente
      schema:
        type: array
        items:
          type: object
          properties:
            id_pasaje:
              type: integer
              example: 1
            precio_total:
              type: float
              example: 100
            fecha_compra:
              type: string
              example: "2000-01-01"
            origen:
              type: string
              example: "Origen"
            destino:
              type: string
              example: "Destino"
            nombre_cliente:
              type: string
              example: "Nombre"
    404:
      description: No tienes boletos

  """
  return TicketController.get_all_tickets_by_id_client()

@ticket_router.route('/ticket/pdf/<int:id_pasaje>/generate', methods=['GET'])
def create_pdf_ticket(id_pasaje):
  """
  Generar el PDF del boleto
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_pasaje
      required: true
      schema:
        type: integer
        example: 1
  responses:
    200:
      description: PDF del boleto
    404:
      description: No se ha encontrado el id seleccionado
  """
  return TicketController.create_pdf_ticket(id_pasaje)

@ticket_router.route('/ticket/pdf/<string:name>', methods=['GET'])
def get_pdf_ticket(name):
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
  return TicketController.get_pdf_ticket(name)