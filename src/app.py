from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from flasgger import Swagger

from services.database import Database
from routes import signup, login, client_router, ticket_router, transaccion_router, discount_router, service_router,general_router,chofer_router,bus_router,terminalCreate_router,ruta_router,asiento_router

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "bd-storedprocedures"  # Secreto para JWT
jwt = JWTManager(app)
CORS(app)

swagger = Swagger(app, template={
  "info": {
    "title": "tourXpress application",
  },
  "securityDefinitions": {
    "BearerAuth": {
      "type": "apiKey",
      "name": "Authorization",
      "in": "header",
      "description": "Introduce el token JWT para autenticar el cliente"
    }
  },
  "security": [{"BearerAuth": []}]
})

db = Database()
db.load_all_procedures()

app.register_blueprint(signup)
app.register_blueprint(login)
app.register_blueprint(client_router)
app.register_blueprint(ticket_router)
app.register_blueprint(transaccion_router)
app.register_blueprint(discount_router)
app.register_blueprint(service_router)
app.register_blueprint(chofer_router)
app.register_blueprint(general_router)
app.register_blueprint(bus_router)
app.register_blueprint(terminalCreate_router)
app.register_blueprint(ruta_router)
app.register_blueprint(asiento_router)

@app.route('/helloworld/public', methods=['GET'])
def helloworld():
  return { "message": "Hello Public World!" }

@app.route('/helloworld/private', methods=['GET'])
@jwt_required()
def helloworld_private():
  return { "message": "Hello Private World!" }

@app.route('/clear-procedures', methods=['GET'])
def clear_procedures():
  Database().delete_all_procedures()
  return jsonify({ 'message': 'Procedimientos eliminados' }), 200

@app.route('/load-triggers', methods=['GET'])
def load_triggers():
  Database().create_triggers()
  return jsonify({ 'message': 'Triggers creados' }), 200
@app.route('/reload-procedures', methods=['GET'])
def reload_procedures():
  Database().delete_all_procedures()
  Database().load_all_procedures()
  return jsonify({ 'message': 'Procedimientos actualizados' }), 200

@app.route('/delete-triggers', methods=['GET'])
def delete_triggers():
  Database().delete_all_triggers()
  return jsonify({ 'message': 'Triggers eliminados' }), 200

@app.route('/reload-triggers', methods=['GET'])
def reload_triggers():
  Database().delete_all_triggers()
  Database().create_triggers()
  return jsonify({ 'message': 'Triggers cargados' }), 200

if __name__ == '__main__':
  app.run(debug=True)
