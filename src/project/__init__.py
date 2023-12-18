from flask import Flask
from bp.home_bp import home_blueprint, db
from bp.sessions_bp import sessions_blueprint
from bp.log_bp import log_blueprint
from bp.err_bp import err_blueprint
from sqlalchemy_utils import database_exists

def create_app(config_filename=None):
    
    app = create_sessions_app(config_filename)

    db_config(app)
    register_blueprints(app)
    return app


def create_sessions_app(config_filename):
    app =  Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    return app


def db_config(app):
    
    db.init_app(app)
    with app.app_context():
        
        # In case there is no db_name database:
        if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
            db.create_all()
    

def register_blueprints(app):
    app.register_blueprint(home_blueprint)
    app.register_blueprint(sessions_blueprint)
    app.register_blueprint(log_blueprint)
    app.register_blueprint(err_blueprint)
