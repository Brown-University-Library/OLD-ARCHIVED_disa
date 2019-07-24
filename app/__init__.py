from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import config


db = SQLAlchemy()
csrf = CSRFProtect(app)
login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app(configName):
    app = Flask(__name__)
    app.config.from_object(config[configName])
    config[configName].init_app(app)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .editor import editor as editor_blueprint
    app.register_blueprint(editor_blueprint, url_prefix='/editor')

    from .dataserv import dataserv as data_blueprint
    app.register_blueprint(data_blueprint, url_prefix='/data')

    return app