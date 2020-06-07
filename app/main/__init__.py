import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt

from .config import config_by_name

from .ressources.authorization import authorization
from .ressources.subscription import subscription
from .ressources.error import error

db = SQLAlchemy()
mm = Marshmallow()
flask_bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    mm.init_app(app)
    flask_bcrypt.init_app(app)

    app.register_blueprint(authorization)
    app.register_blueprint(subscription)
    app.register_blueprint(error)

    return app


app = create_app(os.getenv('ENV') or 'dev')
app.app_context().push()
