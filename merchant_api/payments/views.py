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
        print(token, flush=True)
        shop = MerchantShop.objects.filter(api_token=token).first()
        if shop:
            payments = PaymentRequest.objects.filter(shop=shop, state='PAID', is_transferred=False)
            for payment in payments:
                private_key = get_private_key()
                transfer(payment, shop, private_key)

            return Response({'status': 200})

        raise PermissionDenied


def transfer(payment, shop, private_key):
    # TRANSFERRING
    # payment.is_transferred = True
    # payment.save()
    print('TRANSFER', payment, shop, private_key)


def get_private_key(*args):
    return 'private'
