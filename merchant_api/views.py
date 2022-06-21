from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from merchant_api.settings import config


class FeedbackForm(APIView):

    @swagger_auto_schema(
        operation_description="post parameters to send feedback message",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['name', 'email', 'phone', 'message'],
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'phone': openapi.Schema(type=openapi.TYPE_STRING),
                'message': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        # responses={200: {'result': 'ok'}},

    )
    def post(self, request):
        print(request.data)
        name = request.data.get('name')
        email = request.data.get('email')
        phone_number = request.data.get('phone')
        message = request.data.get('message')
        text = """
            Name: {name}
            E-mail: {email}
            Message: {message}
            Phone: {phone}
            """.format(
            name=name, email=email, phone=phone_number, message=message
        )
        send_mail(
            'Request from rocknblock.io contact form',
            text,
            config.mail_settings.default_from_email,
            [config.mail_settings.feedback_email]
        )
        return Response({'result': 'ok'})
