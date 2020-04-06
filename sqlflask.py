from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os
from flask_mail import Mail, Message

app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir,'test.db')
app.config['JWT_SECRET_KEY'] = 'super-scret'
app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'd1c7c6083ab845'
app.config['MAIL_PASSWORD'] = '93a2facd7a9a0f'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database created!!!!!")


@app.cli.command('db_seed')
def db_seed():
    admin = User(username='admin', email='admin@test.com')
    guest = User(username='guest', email='guest@test.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    print("data is seeded!!!!")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped!!!!!")


@app.route('/userinfos')
def get_user():
    userList = User.query.all()
    result = users_schema.dump(userList)
    return jsonify(result.data)

@app.route('/register', methods=['POST'])
def register_user():

    name = request.form['name']
    email = request.form['email']

    test_email = User.query.filter_by(email=email).first()
    test_username = User.query.filter_by(username=name).first()
    if test_email or test_username:
        return jsonify(message='the email is already exited'),409
    else:
        print(name)
        print(email)
        user = User(username=name, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='Registered'),201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        name = request.json['name']
    else:
        email = request.form['email']
        name = request.form['name']
    print(email)
    print(name)
    test = User.query.filter_by(username=name,email=email).first()
    if test:
        access_token = create_access_token(identity=name)
        return jsonify(message="Login Success", access_token=access_token),200
    else:
        return jsonify(message="You entered bad email or pass"), 401


@app.route('/retrieve_password/<string:email>', methods=['GET'])
def retrieve_password(email):

    user = User.query.filter_by(email=email).first()

    if user:
        msg = Message("You name is " + user.username, sender="admin.noreplay@test.com", recipients=[email])
        mail.send(msg)
        return jsonify(message = "Name send to "+email)
    else:
        return jsonify(message = "Invalid email address")


@app.route('/adduser', methods=['POST'])
@jwt_required
def add_user():

    name = request.form['name']
    mail = request.form['email']
    test = User.query.filter_by(username=name, email=mail).first()
    if test:
        return jsonify(message="User already exits"),409
    else:
        user = User(username=name, email=mail)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User added!!!!"),200


class UserSchema(ma.Schema):
    class Meta:
        fields = ('username','email')

users_schema = UserSchema(many=True)


if __name__ == "__main__":
    app.run(debug=True)
