from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from currency_converter import CurrencyConverter
from merchant_api.consts import CURRENCY_RATE
from merchant_api.payment_requests.models import MerchantShop


class CurrencyExchangeHandler(APIView):

    @swagger_auto_schema(
        operation_description="get USD and EUR currencies rate",
        manual_parameters=[
            openapi.Parameter('api_token', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_STRING),
            openapi.Parameter('currencies', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_ARRAY,
                              items=openapi.Items(type=openapi.TYPE_STRING))],
        # responses={200: PaymentRequestSerializer()},
    )
    def get(self, request):
        is_allowed = MerchantShop.objects.filter(api_token=request.query_params['api_token'])
        if is_allowed:
            converter = CurrencyConverter()
            currencies = request.query_params['currencies'].split(',')
            USD_rate = get_usd_rate()
            result = {}
            for currency in currencies:
                try:
                    rate = converter.convert(1, currency, 'USD')
                    result.update({currency: rate * USD_rate})
                except ValueError as err:
                    raise ValidationError(str(err))

            return Response(result)

        raise PermissionDenied


def get_usd_rate():
    return CURRENCY_RATE['USD']
