from argparse import ArgumentParser
from flask import Flask

app = Flask(__name__)

import api
import config
import json
import os

from api.decorators import api_wrapper

app.config.from_object(config)

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

with app.app_context():
	from api.models import db, Files, Teams, Problems, Solves, Users
	db.init_app(app)
	db.create_all()

app.secret_key = config.SECRET_KEY

app.register_blueprint(api.admin.blueprint, url_prefix="/api/admin")
app.register_blueprint(api.problem.blueprint, url_prefix="/api/problem")
app.register_blueprint(api.stats.blueprint, url_prefix="/api/stats")
app.register_blueprint(api.team.blueprint, url_prefix="/api/team")
app.register_blueprint(api.user.blueprint, url_prefix="/api/user")
api.logger.initialize_logs()

@app.route("/api")
@api_wrapper
def api_main():
	return { "success": 1, "message": "The API is online." }

if __name__ == "__main__":
	with app.app_context():
		parser = ArgumentParser(description="EasyCTF Server Configuration")
		parser.add_argument("-d", "--debug", action="store_true", help="Run the server in debug mode.", default=False)
		args = parser.parse_args()
		keyword_args, _ = dict(args._get_kwargs()), args._get_args()

		app.debug = keyword_args["debug"]
		app.run(host="0.0.0.0", port=8000)
