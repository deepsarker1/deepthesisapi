import threading

from app.logger import LOGGER
import json
from app.wsgi import app
import functools
from app.apis.v1.ai.handler import run_model_and_predict


def ack_message(channel, delivery_tag):
    """Note that `channel` must be the same pika channel instance via which
    the message being ACKed was retrieved (AMQP protocol constraint).
    """
    if channel.is_open:
        channel.basic_ack(delivery_tag)
    else:
        # Channel is already closed, so we can't ACK this message;
        # log and/or do something that makes sense for your app in this case.
        print('Channel closed. Unable to acknowledge')


def handle_message(_, body):
    payload = json.loads(body)
    with app.app_context():
        event_type = payload.get('type')
        data = payload.get('data')
        if event_type == "start_prediction":
            run_model_and_predict(data.get("uuid"))


def do_work(connection, channel, delivery_tag, body, routing_key):
    handle_message(routing_key, body)

    cb = functools.partial(ack_message, channel, delivery_tag)
    connection.add_callback_threadsafe(cb)


def on_message(channel, method_frame, header_frame, body, args):
    (connection, threads) = args
    LOGGER.info('Message Received')
    delivery_tag = method_frame.delivery_tag
    routing_key = method_frame.routing_key
    print(f'{routing_key=}')

    t = threading.Thread(
        target=do_work, args=(connection, channel, delivery_tag, body, routing_key)
    )
    t.start()
    threads.append(t)
