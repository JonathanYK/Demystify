# TODO: at the end of this project, handle the following warning:
# e:\Coding\Demystify\src\env\lib\site-packages\flask_sqlalchemy\__init__.py:872: FSADeprecationWarning: SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be disabled by default in the future.  Set it to True or False to suppress this warning.

import sys

from flask import Flask
sys.path.append('./')
from bp.home_bp import home_blueprint, db
from bp.sessions_bp import sessions_blueprint
from bp.log_bp import log_blueprint
from bp.err_bp import err_blueprint

from sqlalchemy_utils import database_exists

def create_app(config_filename=None):
    
    db_name = 'sessions.db'
    app = create_sessions_app(config_filename, db_name)

    db_config(app, db_name)
    register_blueprints(app)
    return app

def create_sessions_app(config_filename, db_name):
    app =  Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    return app

def db_config(app, db_name):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'
    db.init_app(app)
    
    # in case the're is no db_name database:
    if not database_exists(f'sqlite:///project/{db_name}'):
        db.create_all(app=app)
    
def register_blueprints(app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(sessions_blueprint)
    app.register_blueprint(log_blueprint)    
    app.register_blueprint(err_blueprint)    