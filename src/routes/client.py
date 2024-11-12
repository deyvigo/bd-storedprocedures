from flask import Blueprint

from controllers.client import ClientController

client_router = Blueprint('client', __name__)

@client_router.route('/client/info', methods=['GET'])
def get_all_client_info():
  return ClientController.get_all_client_info()