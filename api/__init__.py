from flask import Flask
import flask_sqlalchemy

from .models import db
from . import config

def create_app():
    flask_app = Flask(__name__)
    
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.DATABASE_TRACK_MODIFICATIONS
    flask_app.app_context().push()
    
    db.init_app(flask_app)
    db.create_all()

    return flask_app