from flask import Blueprint
from controllers.ruta import RutaController

ruta_router = Blueprint('ruta', __name__)
@ruta_router.route('/admin/ruta', methods=['POST'])
def admin_create_route():
  """
  Crear una ruta
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
          duracion_estimada:
            type: time
            example: "04:00:00"
          distancia:
            type: number
            example: 1200
          estado:
            type: string
            example: "Activo"
          id_origen:
            type: integer
            example: 1
          id_destino:
            type: integer
            example: 2
  responses:
    201:
      description: Ruta creada exitosamente
  """
  return RutaController.admin_create_route()

@ruta_router.route('/admin/ruta', methods=['GET'])
def get_ruta_all():
  """
  Obtener todas las rutas
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Rutas obtenidas
    404:
      description: No tienes rutas
  """
  return RutaController.get_ruta_all()

@ruta_router.route('/admin/ruta/<int:id_ruta>', methods=['PUT'])
def update_ruta(id_ruta):
  """
  Actualizar una ruta
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
          duracion_estimada:
            type: time
            example: "04:00:00"
          distancia:
            type: number
            example: 1200
          estado:
            type: string
            example: "Activo"
          id_origen:
            type: integer
            example: 1
          id_destino:
            type: integer
            example: 2
  responses:
    201:
      description: Ruta actualizada exitosamente
  """
  return RutaController.update_ruta(id_ruta)