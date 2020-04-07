from flask import render_template
from app import app

@app.route('/')
def hello():
    return "Howdy"
@app.route('/index')
def index():
    user = {'username':'Ronee'}
    return render_template('index.html', title='Home', user = user)
