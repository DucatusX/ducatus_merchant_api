from merchant_api.payment_requests.models import PaymentRequest, MerchantShop
from merchant_api.payments.models import Payment
from merchant_api.litecoin_rpc import DucatuscoreInterface
from merchant_api.bip32_ducatus import DucatusWallet


def register_payment(tx, address_from, address_to, amount):
    payment_request = PaymentRequest.objects.get(duc_address=address_to)
    payment = Payment(
        payment_request=payment_request,
        tx_hash=tx,
        user_address=address_from,
        amount=amount
    )
    print(
        'PAYMENT: {amount} DUC from {address_from} to {address_to} with TXID: {txid}'.format(
            amount=amount,
            address_from=address_from,
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
    payment_request.save()

    print('payment ok', flush=True)


def parse_payment_message(message):
    # {
    #     "status": "COMMITTED",
    #     "transactionHash": "c0963718ea4bfdf1540cfbbc46357971ac2799f45811505a6a1d8cf8c92b5906",
    #     "userAddress": "1Bwd6WKNykMtsahTSkPaJvw4m4CKXz4hPM",
    #     "amount": 600359,
    #     "currency": "BTC",
    #     "type": "payment",
    #     "success": true
    # }
    tx = message.get('transactionHash')
    address_from = message.get('address_from')
    address_to = message.get('address_to')
    amount = message.get('amount')
    print('PAYMENT:', tx, address_from, address_to, amount, flush=True)

    register_payment(tx, address_from, address_to, amount)


def confirm_transfer(message):
    address_from = message.get('address_from')
    address_to = message.get('address_to')
    shop = MerchantShop.objects.get(duc_address=address_to)
    payment = PaymentRequest.objects.get(shop=shop, duc_address=address_from)
    payment.transfer_state = 'DONE'
    payment.save()
    print('transfer ok', flush=True)


def transfer(payment, shop):
    parity = DucatuscoreInterface()

    amount = payment.received_amount
    address_to = shop.duc_address
    address_from = payment.duc_address

    private_key = get_private_key(shop.root_keys.key_private, payment.cart_id)

    tx = parity.transfer(address_from, private_key, address_to, amount)
    tx = 'tx'

    payment.transfer_state = 'WAITING_FOR_CONFIRMATION'
    payment.transfer_tx = tx
    payment.save()

    print('TRANSFER', payment, shop)


def get_private_key(root_key, cart_id):
    duc_root_key = DucatusWallet.deserialize(root_key)
    child = duc_root_key.get_child(cart_id)
    private = child.private_key.get_key()
    print('first private', private)
    print('second private', child.get_private_key_hex())
    return private
