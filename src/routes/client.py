from flask import Blueprint

from controllers.client import ClientController

client_router = Blueprint('client', __name__)

@client_router.route('/client/info', methods=['GET'])
def get_all_client_info():
  """
  Obtener información del cliente
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Información del cliente
    401:
      description: No autorizado
  """
  return ClientController.get_all_client_info()