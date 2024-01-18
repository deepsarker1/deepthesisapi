from flask_restx import Namespace, fields
from flask import current_app
import pika
import json

api = Namespace('UtilAPIModel')

error_response_model = api.model('ErrorResponseModel', {
    'status': fields.Boolean(False),
    'message': fields.String,
    'error_reason': fields.String
})


def message(status, message):
    response_object = {"status": status, "message": message}
    return response_object


def err_resp(msg, reason, code):
    err = message(False, msg)
    err["error_reason"] = reason
    return err, code


def send_rmq_message_with_pika(data):
    key = "update"

    credentials = pika.PlainCredentials(
        current_app.config.get("MQ_USERNAME"), current_app.config.get("MQ_PASSWORD")
    )

    parameters = pika.ConnectionParameters(
        current_app.config.get("MQ_HOST"), credentials=credentials, heartbeat=5
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(current_app.config.get("MQ_UPDATE_QUEUE"), durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_publish(
        exchange=current_app.config.get("MQ_EXCHANGE"),
        routing_key=key,
        body=json.dumps(data),
    )

    connection.close()