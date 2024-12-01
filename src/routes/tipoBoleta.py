from flask import Blueprint

from controllers.tipoBoleta import TipoBoletaController

tipo_boleta_router = Blueprint('tipo_boleta', __name__)

@tipo_boleta_router.route('/tipo_boleta/<string:tipo>', methods=['GET'])
def get_tipo_boleta_by_tipo(tipo):
  """
  Obtener un tipo de boleta por tipo
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: tipo
      required: true
      schema:
        type: string
        example: "boleta"
  responses:
    200:
      description: Tipo de boleta obtenido
    404:
      description: No hay tipo de boleta con ese tipo
  """

  return TipoBoletaController.get_tipo_boleta_by_tipo(tipo)
