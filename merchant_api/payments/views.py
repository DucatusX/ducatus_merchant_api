from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from merchant_api.payment_requests.models import PaymentRequest, MerchantShop
from merchant_api.payment_requests.serializers import PaymentRequestSerializer


class PaymentTransferHandler(APIView):

    @swagger_auto_schema(
        operation_description="post query for sending all DUC to one endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['api_token'],
            properties={
                'api_token': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        responses={200: PaymentRequestSerializer()},

    )
    def post(self, request):
        token = request.data.get('api_token')
        shop = MerchantShop.objects.filter(api_token=token).first()
        if shop:
            payments = PaymentRequest.objects.filter(shop=shop)
            for payment in payments:
                private_key = get_private_key()
                transfer(payment.duc_address, shop.duc_address, payment.received_amount, private_key)

        raise PermissionDenied

def transfer(*args):
    print('TRANSFER', args)

def get_private_key(*args):
    return 'private'
