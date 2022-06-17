from scanner.eventscanner.queue.pika_handler import send_to_backend
from scanner.models.models import Payment, session
from scanner.scanner.events.block_event import BlockEvent

from merchant_api.settings import config

class DucPaymentMonitor:
    network_type = ['DUCATUS_MAINNET']
    event_type = 'payment'

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_type:
            return

        addresses = block_event.transactions_by_address.keys()
        transfers = session \
            .query(Payment) \
            .filter(Payment.duc_address.in_(addresses)) \
            .distinct(Payment.duc_address) \
            .all()
        for transfer in transfers:
            transactions = block_event.transactions_by_address[transfer.duc_address]

            for transaction in transactions:
                for output in transaction.outputs:
                    if transfer.duc_address not in output.address:
                        print('{}: Found transaction out from internal address. Skip it.'
                              .format(block_event.network.type), flush=True)
                        continue

                    message = {
                        'transactionHash': transaction.tx_hash,
                        'currency': 'DUC',
                        'toAddress': output.address[0],
                        'amount': output.value,
                        'success': True,
                        'status': 'COMMITTED'
                    }

                    send_to_backend(cls.event_type, config.networks.get(block_event.network.type).queue, message)
