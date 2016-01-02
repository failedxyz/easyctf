from argparse import ArgumentParser
from flask import Flask

import api
import config
import json

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER

with app.app_context():
	from api.models import db, Files, Teams, Problems, Solves, Users
	db.init_app(app)
	db.create_all()

app.secret_key = config.SECRET_KEY

app.register_blueprint(api.admin.blueprint, url_prefix="/api/admin")
app.register_blueprint(api.user.blueprint, url_prefix="/api/user")
app.register_blueprint(api.problem.blueprint, url_prefix="/api/problem")
api.logger.initialize_logs()

@app.route("/api")
def api_main():
	return json.dumps({ "success": 1, "message": "The API is online." })

if __name__ == "__main__":
	with app.app_context():
		parser = ArgumentParser(description="EasyCTF Server Configuration")
		parser.add_argument("-d", "--debug", action="store_true", help="Run the server in debug mode.", default=False)
		args = parser.parse_args()
		keyword_args, _ = dict(args._get_kwargs()), args._get_args()

		app.debug = keyword_args["debug"]
		app.run(host="0.0.0.0", port=8000)
