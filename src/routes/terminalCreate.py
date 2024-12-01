from flask import Blueprint
from controllers.terminalCreate import TerminalCreateController

terminalCreate_router = Blueprint('terminalCreate', __name__)

@terminalCreate_router.route('/admin/terminal', methods=['POST'])
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
  return TerminalCreateController.admin_create_terminal()

@terminalCreate_router.route('/admin/terminal', methods=['GET'])
def get_admin_all_terminal():
  """
  Obtener todos los buses
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Terminales obtenidos
    404:
      description: No tienes terminales
  """
  return TerminalCreateController.get_admin_all_terminal()

@terminalCreate_router.route('/admin/terminal/<int:id_terminal>', methods=['PUT'])
def update_terminal(id_terminal):
  """
  Actualizar un terminal
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
      description: Terminal actualizado exitosamente
            
        """
  
  return TerminalCreateController.update_terminal(id_terminal)
