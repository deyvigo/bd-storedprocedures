from flask import Blueprint

from controllers.service import ServiceController

service_router = Blueprint('service', __name__)

@service_router.route('/service', methods=['GET'])
def get_all_services():
  """
  Obtener todos los servicios
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Servicios obtenidos
    404:
      description: No tienes servicios
  """
  return ServiceController.get_all_services()

@service_router.route('/service', methods=['POST'])
def create_service():
  """
  Crear un servicio
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
          servicio:
            type: string
            example: "premium"
  responses:
    201:
      description: Servicio creado
    400:
      description: Error al crear el servicio
  """
  return ServiceController.create_service()

@service_router.route('/service/<int:id_servicio>', methods=['PUT'])
def edit_service(id_servicio):
  """
  Actualizar un servicio
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_servicio
      required: true
      schema:
        type: integer
        example: 1
  responses:
    200:
      description: Servicio actualizado
    400:
      description: Error al actualizar el servicio
  """
  return ServiceController.edit_service(id_servicio)
