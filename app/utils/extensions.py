from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from rabbitmq_pika_flask import RabbitMQ

db = SQLAlchemy()
migrate = Migrate()
rabbit = RabbitMQ()
