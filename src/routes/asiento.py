from flask import Blueprint
from controllers.asiento import AsientoController

asiento_router = Blueprint('asiento', __name__)

@asiento_router.route('/admin/asiento', methods=['POST'])
def admin_create_asiento():
  """
  Crear un asiento
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
          nivel:
            type: integer
            example: 1
          numero:
            type: integer
            example: 25
          id_bus:
            type: integer
            example: 1
  responses:
    201:
      description: Asiento creado exitosamente
  """
  return AsientoController.admin_create_asiento()
@asiento_router.route('/admin/asiento', methods=['GET'])
def admin_get_asiento():
  """
  Obtener todos los asientos
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Lista de asientos
  """
  return AsientoController.admin_get_asiento()

@asiento_router.route('/admin/asiento/<int:id_asiento>', methods=['PUT'])
def update_asiento(id_asiento):
  """
  Actualizar un asiento
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_asiento
      required: true
      type: integer
    - in: body
      name: body
      required: true
      schema:
        type: object
        properties:
          nivel:
            type: integer
            example: 1
          numero:
            type: integer
            example: 25
          id_bus:
            type: integer
            example: 1
  responses:
    200:
      description: Asiento actualizado exitosamente
    404:
      description: Asiento no encontrado
  """
  return AsientoController.update_asiento(id_asiento)

# @admin_router.route('/admin/parada-intermedia', methods=['POST'])
# def admin_create_parada():
#   """
#   Crear una parada intermedia
#   ---
#   tags:
#     - Protegido
#   security:
#     - BearerAuth: []
#   parameters:
#     - in: body
#       name: body
#       required: true
#       schema:
#         type: object
#         properties:
#           ordinal:
#             type: integer
#             example: 1
#           id_terminal:
#             type: integer
#             example: 1
#           id_ruta:
#             type: integer
#             example: 2
#   responses:
#     201:
#       description: Parada intermedia creada exitosamente
#   """
#   return AdminController.admin_create_parada()