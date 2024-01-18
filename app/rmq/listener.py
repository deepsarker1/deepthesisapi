import pika
from flask import current_app
import functools

from app import create_app
from app.logger import LOGGER


# Listen to RabbitMQ
def rmq_listening():
    credentials = pika.PlainCredentials(
        current_app.config['MQ_USERNAME'], current_app.config['MQ_PASSWORD']
    )
    parameters = pika.ConnectionParameters(
        current_app.config['MQ_HOST'], credentials=credentials, heartbeat=5
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(
        exchange=current_app.config['MQ_EXCHANGE'], exchange_type='topic'
    )
    channel.queue_declare(current_app.config['MQ_UPDATE_QUEUE'], durable=True)
    channel.queue_bind(
        queue=current_app.config['MQ_UPDATE_QUEUE'],
        exchange=current_app.config['MQ_EXCHANGE'],
        routing_key='update',
    )

    channel.basic_qos(prefetch_count=1)

    threads = []
    on_message_callback = functools.partial(on_message, args=(connection, threads))
    channel.basic_consume(current_app.config['MQ_UPDATE_QUEUE'], on_message_callback)

    try:
        LOGGER.info('Started consuming...')
        channel.start_consuming()
    except KeyboardInterrupt:
        LOGGER.info(f"Threads called: {len(threads)}")
        channel.stop_consuming()

    # Wait for all to complete
    for thread in threads:
        thread.join()

    connection.close()


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        from app.rmq.utils import on_message

        rmq_listening()
