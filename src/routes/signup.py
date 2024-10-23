from flask import Blueprint

from controllers.signup import SignUpController

signup = Blueprint('signup', __name__)

@signup.route('/signup/admin', methods=['POST'])
def signup_admin():
  return SignUpController.signup_admin()

@signup.route('/signup/client', methods=['POST'])
def signup_client():
  return SignUpController.signup_client()