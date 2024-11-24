from flask import Blueprint

from controllers.general import ControllerGeneral
general_router = Blueprint('general', __name__)

@general_router.route('/general/destination', methods=['POST'])
def get_destination_by_city():
  """
    Obtener ciudades de destino de una ciudad
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
            ciudad_origen:
              type: string
              example: "Lima"
    responses:
      200:
        description: Ciudades de destino
        schema:
          type: array
          items:
            type: object
            properties:
              ciudad_destino:
                type: string
                example: "Ica"
    """
  return ControllerGeneral.get_destination_by_city()

@general_router.route('/general/seat', methods=['POST'])
def get_seat_by_trip():
  """
  Obtener asientos de un viaje programado
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
          id_viaje_programado:
            type: integer
            example: 1
  responses:
    200:
      description: Asientos del bus del viaje
      schema:
        type: array
        items:
          type: object
          properties:
            id_asiento:
              type: integer
              example: 1
            estado:
              type: string  
              example: "disponible"
            nivel:
              type: integer
              example: 1
            numero:
              type: integer
              example: 12
            precio:
              type: float
              example: 100.00
  """
  return ControllerGeneral.get_seat_by_trip()

@general_router.route('/general/scheduled-trip', methods=['POST'])
def get_scheduled_trip():
  """
    Obtener viajes programados
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
            ciudad_origen:
              type: string
              example: "Lima"
            ciudad_destino:
              type: string
              example: "Ancash"
            fecha:
              type: string
              format: date
              example: "2024-11-17"
    responses:
      200:
        description: Viajes programados
        schema:
          type: array
          items:
            type: object
            properties:
              id_viaje_programado:
                type: integer
                example: 1
              origen:
                type: string
                example: "Lima"
              destino:
                type: string
                example: "Ica"
              servicio:
                type: string
                example: "VIP"
              fecha_salida:
                type: string
                format: date
                example: "2022-01-01"
              hora_salida:
                type: string
                format: time
                example: "10:00:00"
              hora_llegada:
                type: string
                format: time
                example: "11:00:00"
              duracion:
                type: integer
                example: 60
              precio_min:
                type: float
                example: 120.00
              asientos_disponibles:
                type: integer
                example: 10
              distancia:
                type: double
                example: 1500
    """
  return ControllerGeneral.get_scheduled_trip()