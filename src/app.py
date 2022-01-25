from unicodedata import name
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST', 'DELETE'])
def index():

    if request.method == 'GET':
        return jsonify({"response is" : "GET request approved!"})

    elif request.method == 'POST':
        req_Json = request.json
        name = req_Json['name']
        return jsonify({"response": "Helllloo " +name})
        


if __name__ == "__main__":
    app.run(debug=True)