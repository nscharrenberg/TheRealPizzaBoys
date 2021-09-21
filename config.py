import os
class Config(object):
    DEBUG = os.getenv("ENVIRONMENT") == "DEV"
    HOST = os.getenv("FLASK_RUN_HOST")
    PORT = int(os.getenv("FLASK_RUN_PORT", "3000"))
    LOCAL_DB = os.getenv("DB_DRIVER", "MYSQL")
    API_PREFIX = os.getenv("API_PREFIX", "/api")

    MYSQL = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "3306"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "db": os.getenv("DB_NAME", "pizzaboys")
    }

    SQLALCHEMY_DATABASE_URI = "mysql://%(user)s:%(password)s@%(host)s:%(port)s/%(db)s" % MYSQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False