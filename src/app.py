from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

from services.database import Database
from routes import signup, login

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "bd-storedprocedures"  # Secreto para JWT
jwt = JWTManager(app)
CORS(app)

db = Database()
db.load_all_procedures()

app.register_blueprint(signup)
app.register_blueprint(login)

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

if __name__ == '__main__':
  app.run(debug=True)