from django.conf.urls import url

from merchant_api.payment_requests.views import PaymentRequest

urlpatterns = [
    url(r'^$', PaymentRequest.as_view(), name='create-exchange-request'),
]