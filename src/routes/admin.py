from flask import Blueprint
from controllers.admin import AdminController

admin_router = Blueprint('admin', __name__)

@admin_router.route('/admin/terminal', methods=['POST'])
def create_admin_terminal():
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
      schema:
        type: object
  """
  return AdminController.create_admin_terminal()

#ruta para crear bus
@admin_router.route('/admin/bus', methods=['POST'])
def admin_create_bus():
  """
  
  
  """
  return AdminController.admin_create_bus()
