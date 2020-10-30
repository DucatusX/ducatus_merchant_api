from merchant_api.payment_requests.models import PaymentRequest, MerchantShop
from merchant_api.payments.models import Payment
from merchant_api.litecoin_rpc import DucatuscoreInterface
from merchant_api.bip32_ducatus import DucatusWallet


def register_payment(tx, address_to, amount):
    payment_request = PaymentRequest.objects.get(duc_address=address_to)
    if payment_request.state != 'PAID':
        payment = Payment(
            payment_request=payment_request,
            tx_hash=tx,
            user_address=address_to,
            amount=amount
        )
        print(
            'PAYMENT: {amount} DUC to {address_to} with TXID: {txid}'.format(
                amount=amount,
                address_to=address_to,
                txid=tx
            ),
            flush=True
        )

        payment.save()
        payment_request.received_amount += payment.amount
        amount_diff = payment_request.original_amount - payment_request.received_amount
        payment_request.remained_amount = amount_diff if amount_diff >= 0 else 0
        if payment_request.remained_amount == 0:
            payment_request.state = 'PAID'
        else:
            payment_request.state = 'PAID_PARTIALLY'
        payment_request.save()

        print('payment ok', flush=True)
    else:
        print('already paid', flush=True)


def parse_payment_message(message):
    tx = message.get('transactionHash')
    address_to = message.get('toAddress')
    amount = message.get('amount')
    print('PAYMENT:', tx, address_to, amount, flush=True)

    register_payment(tx, address_to, amount)


def parse_transfer_messager(message):
    tx_hash = message.get('txHash')
    # address_from = message.get('address_from')
    # address_to = message.get('toAddress')
    # shop = MerchantShop.objects.get(duc_address=address_to)
    payment_request = PaymentRequest.objects.get(transfer_tx=tx_hash)
    payment_request.transfer_state = 'DONE'
    payment_request.save()
    print('transfer ok', flush=True)


def transfer(payment, shop):
    rpc = DucatuscoreInterface()

    amount = payment.received_amount
    address_to = shop.duc_address
    address_from = payment.duc_address

    print('Starting transfer', address_from, 'to', address_to, 'amount', amount, flush=True)

    private_key = get_private_key(shop.root_keys.key_private, payment.cart_id)

    prev_tx_list = list(Payment.objects.filter(payment_request=payment).values_list('tx_hash', flat=True))

    try:
        tx = rpc.internal_transfer(prev_tx_list, address_from, address_to, amount, private_key)
        payment.transfer_state = 'WAITING_FOR_CONFIRMATION'
        payment.transfer_tx = tx
        payment.save()
    except Exception as e:
        print('Error in internal transfer from {addr_from} to {addr_to} with amount {amount} DUC'.format(
            addr_from=address_from,
            addr_to=address_to,
            amount=amount
        ), flush=True)
        print('error:', e, flush=True)



def get_private_key(root_key, cart_id):
    duc_root_key = DucatusWallet.deserialize(root_key)
    child = duc_root_key.get_child(cart_id)
    private = child.export_to_wif().decode()
    print('child private', private)
    return private
