from flask import Flask
import sys

app = Flask(__name__)

#Home Page
@app.route("/")
def hello_world():
	return "Hello, EasyCTF!"
#Login Page
@app.route('/login')
def login():
	return "EasyCTF Login"
#Registration Page
@app.route('/register')
def register():
	return "EasyCTF Register"
#Scoreboard Page
@app.route('/scoreboard')
def scoreboard():
	return "EasyCTF Scoreboard"
#Problems Page
@app.route('/problems')
def problems():
	return "EasyCTF Problems"

if __name__ == "__main__":
    app.debug = "--debug" in sys.argv
    app.run(port=8000)
