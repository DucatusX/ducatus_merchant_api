from merchant_api.payment_requests.models import PaymentRequest
from merchant_api.payments.models import Payment


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
    if payment_request.received_amount >= payment_request.original_amount:
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
    pass
