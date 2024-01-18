from dotenv import load_dotenv
from os import environ
from pathlib import Path
import os

load_dotenv()


class BaseConfig:
    BASE_DIR = Path(__file__).parent.parent
    TESTING = False
    FLASK_CONFIG = environ.get("FLASK_CONFIG", "development")
    MQ_EXCHANGE = environ.get('MQ_EXCHANGE')
    MQ_JOB_QUEUE = environ.get('MQ_JOB_QUEUE')
    MQ_UPDATE_QUEUE = environ.get('MQ_UPDATE_QUEUE')
    MQ_USERNAME = environ.get('MQ_USERNAME')
    MQ_PASSWORD = environ.get('MQ_PASSWORD')
    MQ_HOST = environ.get('MQ_HOST')
    MQ_PORT = environ.get('MQ_PORT')
    MQ_URL = f"amqp://{MQ_USERNAME}:{MQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}/"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = environ.get(
        "SQLALCHEMY_DATABASE_URI"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

