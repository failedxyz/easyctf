import datetime
import logging
import logging.handlers
import os

NOTSET = 0
DEBUG = 10
INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50

def initialize_logs():
    registration_logger = logging.getLogger("registrations")
    login_logger = logging.getLogger("logins")
    submission_logger = logging.getLogger("submissions")

    registration_logger.setLevel(logging.INFO)
    login_logger.setLevel(logging.INFO)
    submission_logger.setLevel(logging.INFO)

    base = os.path.dirname(__file__).strip("api")
    log_path = os.path.join(base, "logs")

    if not os.path.exists(log_path):
        os.mkdir(log_path)

    # logs = [os.path.join(log_path, "registrations.log"), os.path.join(log_path, "logins.log"), os.path.join(log_path, "submissions.log")]
    logs = map(lambda x: os.path.join(log_path, x + ".log"), \
        [ "registrations", "logins", "submissions", "create_team" ])

    registration_log = logging.handlers.RotatingFileHandler(logs[0], maxBytes=10000)
    login_log = logging.handlers.RotatingFileHandler(logs[1], maxBytes=10000)
    submission_log = logging.handlers.RotatingFileHandler(logs[2], maxBytes=10000)

    registration_logger.addHandler(registration_log)
    login_logger.addHandler(login_log)
    submission_logger.addHandler(submission_log)

def log(log, level, message):
    logger = logging.getLogger(log)
    message = "[%s] %s" % (datetime.datetime.now().strftime("%m/%d/%Y %X"), message)
    logger.log(level, message)
