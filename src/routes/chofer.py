from flask import Blueprint


from controllers.chofer import ChoferController

chofer_router = Blueprint('chofer_router',__name__)

@chofer_router.route("/chofer/hired",methods=['GET'])
def get_all_chofer():
  """
  Obtener todos los choferes contratados
  ---
  tags:
    - Protegido
  security:
    - BearerAuth: []
  responses:  
    200:
      description: Choferes obtenidos
      schema:
        type: array
        items:
          type: object
          properties:
            id_chofer:
              type: integer
              example: 1
            nombre:
              type: string
              example: "Chofer 1"
            apellido_pat:
              type: string
              example: "ApellidoPaterno"
            apellido_mat:
              type: string 
              example: "ApellidoMaterno"
            dni:
              type: string
              example: "12345678"
            sexo:
              type: string
              example: "masculino"
            estado:
              type: string
              values:
                type: string
              example: "contratado"
    404:
      description: Choferes no encontrados
    500:
      description: No se pudo obtener los choferes contratados
  """
  return ChoferController.get_all_hired_choferes()

@chofer_router.route("/chofer/create",methods=['POST'])
def post_chofer(): 
  """
  Crear un chofer
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
            example: "Chofer1"
          apellido_pat:
            type: string
            example: "ApellidoPaterno"
          apellido_mat:
            type: string 
            example: "ApellidoMaterno"
          dni:
            type: string
            example: "12345678"
          sexo:
            type: string
            example: "masculino"
  responses:
    201:
      description: Chofer creado
    400:
      description: Error al crear el chofer
    500:
      description: No se pudo crear el chofer 
  """
  return ChoferController.register_chofer()

@chofer_router.route("/chofer/status",methods=['PATCH'])
def update_status_chofer():
  """
  Actualizar el estado de un chofer
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
          id_chofer:
            type: integer
            example: 1
  responses:
    200:
      description: Chofer actualizado
    400:
      description: Error al actualizar el chofer
    500:
      description: No se pudo actualizar el chofer
  """
  return ChoferController.update_status_chofer()

@chofer_router.route("/chofer/update",methods=['PATCH'])
def update_chofer_info(): 
  """
  Actualizar datos de un chofer
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
          id_chofer:
            type: integer
            example: 1
          nombre:
            type: string
            example: "Chofer1"
          apellido_pat:
            type: string
            example: "ApellidoPaterno"
          apellido_mat:
            type: string
            example: "ApellidoMaterno"
          dni: 
            type: string
            example: "12345678"
          sexo:
            type: string
            example: "masculino"
  responses:
    200:
      description: Chofer actualizado
    400:
      description: Error al actualizar el chofer
    500:
      description: No se pudo actualizar el chofer  
  """
  return ChoferController.update_chofer()

@chofer_router.route("/chofer/free",methods=['POST'])  
def get_free_choferes():
  """
  Obtener todos los choferes libres
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
          date:
            type: string
            example: "2024-11-24"
  responses:
    200:
      description: Choferes obtenidos
    404:
      description: No hay choferes libres en la fecha seleccionada
    500:
      description: No se pudo obtener los choferes contratados
  """
  return ChoferController.get_free_choferes()