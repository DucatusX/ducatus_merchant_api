from django.conf.urls import url

from merchant_api.payments.views import PaymentTransferHandler

urlpatterns = [
    url(r'^$', PaymentTransferHandler.as_view(), name='create-transfer-request'),
]
