from django.conf.urls import url

from merchant_api.rates.api import CurrencyExchangeHandler

urlpatterns = [
    url(r'^$', CurrencyExchangeHandler.as_view(), name='create-payment-request'),
]
