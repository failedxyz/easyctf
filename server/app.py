from flask import Flask

import sys

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
if __name__ == "__main__":
    app.debug = "--debug" in sys.argv
    app.run(port=8000)
