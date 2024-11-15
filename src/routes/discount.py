from flask import Blueprint

from controllers.discount import DiscountController

discount_router = Blueprint('discount', __name__)

@discount_router.route('/discount', methods=['POST'])
def create_discount():
  """
  Crear un descuento
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
          codigo:
            type: string
            example: "DESC50"
          monto:
            type: number
            example: 50.00
          estado:
            type: string
            example: "activo"
  responses:
    201:
      description: Descuento creado
    400:
      description: Error al crear el descuento
  """
  return DiscountController.create_discount()

@discount_router.route('/discount', methods=['GET'])
def get_all_discounts():
  """
  Obtener todos los descuentos
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:
    200:
      description: Descuentos obtenidos
    404:
      description: No tienes descuentos
  """
  return DiscountController.get_all_discounts()

@discount_router.route('/discount/<int:id_descuento>', methods=['PUT'])
def edit_discount(id_descuento):
  """
  Actualizar un descuento
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  parameters:
    - in: path
      name: id_descuento
      required: true
      schema:
        type: integer
        example: 1
  responses:
    200:
      description: Descuento actualizado
    400:
      description: Error al actualizar el descuento
  """
  return DiscountController.edit_discount(id_descuento)
