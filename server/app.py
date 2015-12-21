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
#Account Page
@app.route('/account')
def account():
	return "EasyCTF Account"
#Programming Page
@app.route('/programming')
def programming():
	return "EasyCTF Programming"
#Chat Page
@app.route('/chat')
def chat():
	return "EasyCTF Chat"
#About Page
@app.route('/about')
def about():
	return "EasyCTF About"
#Forgot Password Page
@app.route('/forgot_password')
def forgot_password():
	return "EasyCTF Forgot Password"
#Logout Page
@app.route('/logout')
def logout():
	return "EasyCTF Logout"
#Rules Page
@app.route('/rules')
def rules():
	return "EasyCTF Rules"
#Team Page
@app.route('/team')
def team():
	return "EasyCTF Team"
#Shell Page
@app.route('/shell')
def shell():
	return "EasyCTF Shell"
#Updates Page
@app.route('/updates')
def updates():
	return "EasyCTF Updates"
#Reset Password Page
@app.route('/reset_password')
def reset_password():
	return "EasyCTF Reset"

if __name__ == "__main__":
    app.debug = "--debug" in sys.argv
    app.run(port=8000)
