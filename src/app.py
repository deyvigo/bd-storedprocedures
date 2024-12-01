from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

from services.database import Database
from routes import signup, login, general_router, ticket_router, transaccion_router, client_router, chofer_router

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "bd-storedprocedures"  # Secreto para JWT
jwt = JWTManager(app)
CORS(app)

db = Database()
db.load_all_procedures()

app.register_blueprint(signup)
app.register_blueprint(login)
app.register_blueprint(general_router)
app.register_blueprint(ticket_router)
app.register_blueprint(transaccion_router)
app.register_blueprint(client_router)
app.register_blueprint(chofer_router)

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


@app.route('/reload-procedures', methods=['GET'])
def reload_procedures():
  Database().delete_all_procedures()
  Database().load_all_procedures()
  return jsonify({ 'message': 'Procedimientos cargados' }), 200

if __name__ == '__main__':
  app.run(debug=True)