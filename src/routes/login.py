from flask import Blueprint

from controllers.login import LoginController

login = Blueprint('login', __name__)

@login.route('/login/admin', methods=['POST'])
def login_admin():
  return LoginController.login_admin()

@login.route('/login/client', methods=['POST'])
def login_client():
  return LoginController.login_client()