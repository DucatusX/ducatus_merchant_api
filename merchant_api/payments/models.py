from django.db import models

from merchant_api.consts import MAX_DIGITS
from merchant_api.payment_requests.models import PaymentRequest


class Payment(models.Model):
    payment_request = models.ForeignKey(PaymentRequest, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=100, null=True, default='')
    user_address = models.CharField(max_length=50, null=True, default=None)
    amount = models.DecimalField(max_digits=MAX_DIGITS, decimal_places=0)
    created_date = models.DateTimeField(auto_now_add=True)
