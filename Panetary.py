from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Column
import os


app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLAlCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(baseDir,'planets.db')

db = SQLAlchemy(app)

# create queries

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Data base is created")

@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Data is dropped")

@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class M',
                     home_star = 'Sun',
                     mass = 1.2,
                     radius = 1.3,
                     distance = 1.4)

    db.session.add(mercury)
    db.session.commit()

    print('databse seeded!!!!')


# database models


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column('todo_id', db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    text = db.Column(db.String)
    done = db.Column(db.Boolean)

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False


class User(db.Model):

    __table_name__ = 'users'
    id = Column(Integer, primary_key = True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique = True)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = 'Planets'
    planet_id = db.Column(Integer, primary_key = True)
    planet_name = db.Column(String)
    planet_type = db.Column(String)
    home_star = db.Column(String)
    mass = db.Column(Float)
    radius = db.Column(Float)
    distance = db.Column(Float)

@app.route('/')
def hello_world():
    return "Hello world"

if __name__=="__main__":
    app.run(debug=True)
