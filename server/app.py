from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
	return "Hello, EasyCTF!"

@app.route('/login')
def login():
	return
@app.route('/register')
def register():
	return
@app.route('/scoreboard')
def scoreboard():
	return
@app.route('/problems')
def problems():
	return

app.run(port=8000)
