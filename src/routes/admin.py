from flask import Blueprint

from controllers.admin import AdminController

admin_router = Blueprint('admin', __name__)

@admin_router.route('/admin/info', methods=['GET'])
def get_admin_info():
  return AdminController.get_admin_info()
