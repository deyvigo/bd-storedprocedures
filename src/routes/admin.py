from flask import Blueprint
from controllers.adminCreate import AdminController

admin_router = Blueprint('admin', __name__)

@admin_router.route('/admin/terminal', methods=['POST'])
def admin_create_terminal():
  """
  Crear una terminal
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
            example: "Terminal 1"
          departamento:
            type: string
            example: "Lima"
          provincia:
            type: string
            example: "Lima"
  responses:
    201:
      description: Terminal creada exitosamente
  """
  return AdminController.admin_create_terminal()

@admin_router.route('/admin/bus', methods=['POST'])
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
  return AdminController.admin_create_bus()

@admin_router.route('/admin/asiento', methods=['POST'])
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
  return AdminController.admin_create_asiento()

@admin_router.route('/admin/ruta', methods=['POST'])
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
  return AdminController.admin_create_route()

@admin_router.route('/admin/parada-intermedia', methods=['POST'])
def admin_create_parada():
  """
  Crear una parada intermedia
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
          ordinal:
            type: integer
            example: 1
          id_terminal:
            type: integer
            example: 1
          id_ruta:
            type: integer
            example: 2
  responses:
    201:
      description: Parada intermedia creada exitosamente
  """
  return AdminController.admin_create_parada()