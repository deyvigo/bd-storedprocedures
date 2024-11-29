from flask import Blueprint

from controllers.terminal import TerminalController


terminal_router = Blueprint('terminal', __name__)

@terminal_router.route('/terminal/departamento', methods=['GET'])
def get_departamento_terminal():
  return TerminalController.get_all_departamento_terminal()
