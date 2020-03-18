from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


from merchant_api.payment_requests.models import PaymentRequest
from merchant_api.bip32_ducatus import DucatusWallet



class PaymentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRequest
        fields = ['shop', 'cart_id', 'original_amount', 'received_amount', 'duc_address', 'state', 'created_at',
                  'is_transferred', 'remained_amount']

    def create(self, validated_data):
        print('validated_data:', validated_data, flush=True)
        shop = validated_data['shop']
        cart_id = validated_data['cart_id']

        shop_root_key = DucatusWallet.deserialize(shop.root_keys.key_public)
        duc_address = shop_root_key.get_child(cart_id, is_prime=False).to_address()

        validated_data['duc_address'] = duc_address
        validated_data['remained_amount'] = validated_data['original_amount']

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

    def to_representation(self, payment_info):
        result = super().to_representation(payment_info)
        return result
