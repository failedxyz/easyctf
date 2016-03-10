#!/usr/bin/python

from argparse import ArgumentParser
from flask import Flask

app = Flask(__name__)

import api
import config
import json
import logging
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

def run(args):
	with app.app_context():
		app.debug = keyword_args["debug"]
		app.run(host="0.0.0.0", port=8000)

def load_problems(args):
	if not os.path.exists(config.PROBLEM_DIR):
		logging.critical("Problems directory doesn't exist.")
		return

	for (dirpath, dirnames, filenames) in os.walk(config.PROBLEM_DIR):
		if "problem.json" in filenames:
			json_file = os.path.join(dirpath, "problem.json")
			contents = open(json_file).read()

			try:
				data = json.loads(contents)
			except ValueError as e:
				logging.warning("Invalid JSON format in file {filename} ({exception})".format(filename=json_file, exception=e))
				continue

			if not isinstance(data, dict):
				logging.warning("{filename} is not a dict.".format(filename=json_file))
				continue

			missing_keys = []
			for key in ["pid", "title", "category", "value"]:
				if key not in data:
					missing_keys.append(key)
			if len(missing_keys) > 0:
				logging.warning("{filename} is missing the following keys: {keys}".format(filename=json_file, keys=", ".join(missing_keys)))
				continue

			relative_path = os.path.relpath(dirpath, config.PROBLEM_DIR)
			logging.info("Found problem '{}'".format(data["title"]))

			try:
				api.problem.insert_problem(data)
			except Exception as e:
				logging.warning("Problem '{}' was not added to the database. Error: {}".format(data["title"], e))

if __name__ == "__main__":
	parser = ArgumentParser(description="EasyCTF Server Management")

	subparser = parser.add_subparsers(help="Select one of the following actions.")
	parser_problems = subparser.add_parser("problems", help="Manage problems.")
	subparser_problems = parser_problems.add_subparsers(help="Select one of the following actions.")
	parser_problems_load = subparser_problems.add_parser("load", help="Load all problems into database.")
	parser_problems_load.set_defaults(func=load_problems)

	parser_run = subparser.add_parser("run", help="Run the server.")
	parser_run.add_argument("-d", "--debug", action="store_true", help="Run the server in debug mode.", default=False)
	parser_run.set_defaults(func=run)

	args = parser.parse_args()
	keyword_args, _ = dict(args._get_kwargs()), args._get_args()
	logging.getLogger().setLevel(logging.INFO)

	if "func" in args:
		args.func(args)
	else:
		parser.print_help()