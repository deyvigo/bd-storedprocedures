from flask import Flask, jsonify
from flask_cors import CORS
from services.connection import Connection

app = Flask(__name__)

CORS(app)

@app.route('/helloworld')
def helloworld():
  connection = Connection()
  return { "message": "Hello World!" }


if __name__ == '__main__':
  app.run(debug=True)