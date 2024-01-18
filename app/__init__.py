from flask import Flask
from os import environ
from .utils.extensions import db, migrate, rabbit
from .apis.v1 import blueprint_v1
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app_settings = environ.get("APP_SETTINGS", "app.config.DevelopmentConfig")
    app.config.from_object(app_settings)
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_size": 100,
        "pool_recycle": 280
    }
    register_extensions(app)
    app.register_blueprint(blueprint_v1)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    rabbit.init_app(app, app.config.get('MQ_JOB_QUEUE'))
