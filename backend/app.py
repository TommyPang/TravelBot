from flask import Flask, request, jsonify
from util import *
from chatbot import *
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.debug = True

vectordb = initialize_vector_db()

@app.route("/api/query", methods=["POST"])
def query():
    prompt = request.get_json()['prompt']
    try:
        response = chatbot_response(prompt, vectordb)
        return jsonify({"message": response}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "chatbot query failed, please try again later"}), 500

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8000)