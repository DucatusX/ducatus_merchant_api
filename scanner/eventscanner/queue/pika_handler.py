import os
import pika
import json


def send_to_backend(type, queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        'rabbitmq',
        5672,
        os.getenv('RABBITMQ_DEFAULT_VHOST', 'merchant_api'),
        pika.PlainCredentials(
            os.getenv('RABBITMQ_DEFAULT_USER', 'merchant_api'),
            os.getenv('RABBITMQ_DEFAULT_PASS', 'merchant_api')
        ),
    ))
    channel = connection.channel()
    channel.queue_declare(queue=queue, durable=True, auto_delete=False,
                          exclusive=False)
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(type=type),
    )
    connection.close()

    print('message sent to backend: {}'.format(message), flush=True)


def send_to_monitor():
    pass
