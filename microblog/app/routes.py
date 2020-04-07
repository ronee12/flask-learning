from app import app
@app.route('/')
def hello():
    return "Howdy"
@app.route('/index')
def index():
    return 'Hello world'
