import requests
import os
import hashlib
import binascii

from bip32utils import BIP32Key
from eth_keys import keys
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from merchant_api.settings import ROOT_KEYS, BITCOIN_URLS, IS_TESTNET_PAYMENTS
from merchant_api.payment_requests.models import PaymentRequest
from merchant_api.rates.api import convert_to_duc_single, get_usd_rates
from merchant_api.bip32_ducatus import DucatusWallet


def registration_btc_address(btc_address):
    requests.post(
        BITCOIN_URLS['main'],
        json={
            'method': 'importaddress',
            'params': [btc_address, btc_address, False],
            'id': 1, 'jsonrpc': '1.0'
        }
    )


class ExchangeRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ['shop', 'cart_id', 'original_amount', 'receive_amount']

    def create(self, validated_data):
        print('validated_data:', validated_data, flush=True)
        shop = validated_data['shop']
        cart_id = validated_data['cart_id']

        shop_root_key = DucatusWallet.deserialize(shop.root_keys.key_public)
        duc_address = shop_root_key.get_child(cart_id, is_prime=False).to_address()

        validated_data['duc_address'] = duc_address

        return super().create(validated_data)

    def is_valid(self, raise_exception=False):
        if hasattr(self, 'initial_data'):
            try:
                obj = PaymentRequest.objects.get(**self.initial_data)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                return super().is_valid(raise_exception)
            else:
                self.instance = obj
                return super().is_valid(raise_exception)
        else:
            return super().is_valid(raise_exception)
