from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import routes
from flask.blueprints import Blueprint

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


for blueprint in vars(routes).values():
    if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint, url_prefix=Config.API_PREFIX + "/" + blueprint.name)


if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT)
