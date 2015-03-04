from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext import restful
from flask.ext.restful import reqparse, Api
from flask.ext.httpauth import HTTPBasicAuth
from config import config

db = SQLAlchemy()
mail = Mail()
api = restful.Api(prefix='/api/v1')
auth = HTTPBasicAuth()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from . import account
    #from .account import views #as auth_blueprint
    #app.register_blueprint(auth_blueprint)

    from .resource import resource as resource_blueprint
    app.register_blueprint(resource_blueprint)

    api.init_app(app)

    return app
