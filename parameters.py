from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(message='Hello world')


@app.route('/paramters')

def paramters():
    name = request.args.get('name')
    age = int(request.args.get('age'))

    if(age < 18):
        return jsonify(message="Your name is " + name + " and you are not welcome here")
    else:
        return jsonify(message= "Your name is " + name + " We are welcoming you, get in")


@app.route('/variable/<string:name>/<int:age>')
def par(name: str, age: int):

    if(age < 18):
        return jsonify(message="Your name is " + name + " and you are not welcome here")
    else:
        return jsonify(message= "Your name is " + name + " We are welcoming you, get in")

if __name__=="__main__":
    app.run(debug=True)
