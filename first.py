from flask import Flask, jsonify, request

app = Flask(__name__)
@app.route('/')
def hello_world():
    return "Hello world"

@app.route('/sayMyName', methods = ["GET"])
def return_myName():
    return "My Name is Ronee"

@app.route('/addNum', methods = ["POST"])
def addTwoNum():
    dataDict = request.get_json()
    return jsonify(dataDict)

@app.route('/fetchJson')
def deviceData():
    retJson = {
        'name':'Ronee',
        'age': 26,
        'phone': [
            {
            'phone': "Samsung M30S",
            'Ram': "6GB"
            },
            {
            'phone' : "Samsung J2 Core",
            'Ram'   : "1GB"
            }
        ]
    }
    return jsonify(retJson)

if __name__ == "_main_":
    app.run(host="127.0.0.1", port=80)
