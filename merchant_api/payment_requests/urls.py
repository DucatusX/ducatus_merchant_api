from django.conf.urls import url

from merchant_api.payment_requests.views import PaymentRequestHandler

urlpatterns = [
    url(r'^$', PaymentRequestHandler.as_view(), name='create-payment-request'),
]
