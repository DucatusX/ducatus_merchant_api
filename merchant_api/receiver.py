import pika
import os
import traceback
import threading
import json
import sys
from types import FunctionType


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'merchant_api.settings')
import django
django.setup()

from merchant_api.settings import config
from merchant_api.payments.api import parse_payment_message, parse_transfer_messager


class Receiver(threading.Thread):

    def __init__(self, queue):
        super().__init__()
        self.network = queue

    def run(self):
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

        queue_name = config.networks.get(self.network).queue

        channel.queue_declare(
                queue=queue_name,
                durable=True,
                auto_delete=False,
                exclusive=False
        )
        channel.basic_consume(
            queue=queue_name,
            on_message_callback=self.callback
        )

        print(
            'RECEIVER MAIN: started on {net} with queue `{queue_name}`'
            .format(net=self.network, queue_name=queue_name), flush=True
        )

        channel.start_consuming()

    def payment(self, message):
        print('PAYMENT MESSAGE RECEIVED', flush=True)
        parse_payment_message(message)

    def transferred(self, message):
        print('TRANSFER CONFIRMATION RECEIVED', flush=True)
        parse_transfer_messager(message)

    def callback(self, ch, method, properties, body):
        print('received', body, properties, method, flush=True)
        try:
            message = json.loads(body.decode())
            if message.get('status', '') == 'COMMITTED':
                getattr(self, properties.type, self.unknown_handler)(message)
        except Exception as e:
            print('\n'.join(traceback.format_exception(*sys.exc_info())),
                  flush=True)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def unknown_handler(self, message):
        print('unknown message', message, flush=True)


networks = config.networks.keys()


if __name__ == '__main__':
    for network in networks:
        rec = Receiver(network)
        rec.start()
