from flask import Flask, jsonify, request
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(buildingRestful)


def checkPostedData(postedData, functionName):
    if (functionName == "add"):
        if "x" not in postedData or "y" not in postedData:
            return 301
        else:
            return 200
class Add(Resource):
    def post(self):
        postedData = request.get_json()
        x = postedData["x"]
        y = postedData["y"]
        x = int(x)
        y = int(y)
        sum = x+y

        retJson = {
            "Message": sum,
            "Status Code": 200
        }
        return jsonify(retJson)



class subtract(Resource):
    pass
class Multiply(Resource):
    pass
class Divide(Resource):
    pass

api.add_resource(Add, "/add")

@app.route('/')
def hello_world():
    return "Hello World!"


if __name__=="__main__":
    app.run(debug=True)
