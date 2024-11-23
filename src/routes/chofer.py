from flask import Blueprint


from controllers.chofer import ChoferController

chofer_router = Blueprint('chofer_router',__name__)

@chofer_router.route("/chofer/hired",methods=['GET'])
def get_all_chofer():
  """
  """
  return ChoferController.get_all_hired_choferes()

@chofer_router.route("/chofer/create",methods=['POST'])
def post_chofer(): 
  """
  """
  return ChoferController.register_chofer()

@chofer_router.route("/chofer/status",methods=['PATCH'])
def update_status_chofer():
  """
  """
  return ChoferController.update_status_chofer()

@chofer_router.route("/chofer/update",methods=['PATCH'])
def update_chofer_info(): 
  """
  """
  return ChoferController.update_chofer()