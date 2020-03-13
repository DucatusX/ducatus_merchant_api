from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from merchant_api.payment_requests.models import MerchantShop, PaymentRequest
from merchant_api.payment_requests.serializers import PaymentRequestSerializer


class PaymentRequestHandler(APIView):

    @swagger_auto_schema(
        operation_description="post cart id and cart amount to get ducatus address and pay amount",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['cart_id', 'amount', 'api_token'],
            properties={
                'cart_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'original_amount': openapi.Schema(type=openapi.TYPE_STRING),
                'api_token': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        responses={200: PaymentRequestSerializer()},

    )
    def post(self, request):
        request_data = request.data
        token = request_data.get('api_token')

        shop = MerchantShop.objects.get(api_token=token)

        request_data['shop'] = shop.id
        request_data.pop('api_token')

        print('data:', request_data, flush=True)
        serializer = PaymentRequestSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print('res:', serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="get payment status with all payment info",
        manual_parameters=[
            openapi.Parameter('cart_id', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_INTEGER),
            openapi.Parameter('api_token', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING)],
        responses = {200: PaymentRequestSerializer()},
    )

    def get(self, request):
        api_token = request.query_params['api_token']
        cart_id = int(request.query_params['cart_id'])
        shop = MerchantShop.objects.get(api_token=api_token)
        payment_info = PaymentRequest.objects.filter(cart_id=cart_id, shop=shop).last()

        return Response(PaymentRequestSerializer().to_representation(payment_info))
