from scanner.eventscanner.queue.pika_handler import send_to_backend
from scanner.models.models import Payment, session
from scanner.scanner.events.block_event import BlockEvent

from merchant_api.settings import config


class DucTransferMonitor:
    network_type = ['DUCATUS_MAINNET']
    event_type = 'transferred'

    @classmethod
    def on_new_block_event(cls, block_event: BlockEvent):
        if block_event.network.type not in cls.network_type:
            return

        tx_hashes = set()
        for address_transactions in block_event.transactions_by_address.values():
            for transaction in address_transactions:
                tx_hashes.add(transaction.tx_hash)

        transfers = session \
            .query(Payment) \
            .filter(Payment.transfer_tx.in_(tx_hashes)) \
            .distinct(Payment.transfer_tx) \
            .all()
        for transfer in transfers:

            message = {
                'txHash': transfer.transfer_tx,
                'success': True,
                'status': 'COMMITTED'
            }

            send_to_backend(cls.event_type, config.networks.get(block_event.network.type).queue, message)
