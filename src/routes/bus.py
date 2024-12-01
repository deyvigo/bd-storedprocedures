from flask import Blueprint
from controllers.bus import BusController
bus_router = Blueprint('bus', __name__)

@bus_router.route('/admin/bus', methods=['GET'])
def get_admin_all_bus():
  """
  Obtener todos los buses
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Buses obtenidos
    404:
      description: No tienes buses
  """
  return BusController.get_admin_all_bus()

@bus_router.route('/admin/bus', methods=['POST'])
def admin_create_bus():
  """
  Crear un bus
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
          asientos:
            type: integer
            example: 40
          placa:
            type: string
            example: "BCD123"
          marca:
            type: string
            example: "Mercedes-Benz"
          niveles:
            type: integer
            example: 2
          id_tipo_servicio_bus:
            type: integer
            example: 1        
  responses:
    201:
      description: Bus creado exitosamente
  """
  return BusController.admin_create_bus()

@bus_router.route('/admin/bus/<int:id_bus>', methods=['PUT'])
def update_bus(id_bus):
  """
  Actualizar un bus
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_bus
      required: true
      type: integer
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          asientos:
            type: integer
            example: 40
          placa:
            type: string
            example: "BCD123"
          marca:
            type: string
            example: "Mercedes-Benz"
          niveles:
            type: integer
          id_tipo_servicio_bus:
            type: integer
            example: 1        
  responses:
    201:
      description: Bus actualizado exitosamente
            
        """
  
  return BusController.update_bus(id_bus)

