from flask import Flask, jsonify, request
from flask_cors import CORS

from services.database import Database
from routes import signup

app = Flask(__name__)

CORS(app)

db = Database()
db.load_all_procedures()

app.register_blueprint(signup)

@app.route('/helloworld')
def helloworld():
  db = Database()
  return { "message": "Hello World!" }

# @app.route('/procedure/call', methods=['POST'])
# def procedure():
#   data = request.json
#   procedure_name = data.get('procedure_name')
#   arguments = data.get('args', [])

#   if not procedure_name:
#     return jsonify({ 'error': 'El nombre del procedimiento es obligatorio' }), 400

#   query = f'CALL {procedure_name};'.replace('?', '%s')

#   db = Database().connection()
#   with db.cursor() as cursor:
#     cursor.execute(query, arguments)
#     results = { 'rows_affected': cursor.rowcount, 'last_id': cursor.lastrowid }

#   db.commit()

#   if results is not None:
#     return jsonify(results), 200
#   return jsonify({ 'error': 'No se pudo ejecutar el procedimiento' }), 500

if __name__ == '__main__':
  app.run(debug=True)