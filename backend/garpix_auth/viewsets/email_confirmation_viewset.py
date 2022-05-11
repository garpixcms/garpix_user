from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth import settings
from garpix_auth.serializers import EmailConfirmSendSerializer, EmailConfirmCheckCodeSerializer, \
    EmailPreConfirmCheckCodeSerializer, EmailPreConfirmSendSerializer
from garpix_auth.models import UserSession

User = get_user_model()


class EmailConfirmationViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return EmailConfirmSendSerializer
        return EmailPreConfirmCheckCodeSerializer

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = EmailConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = request.data('email', None)
            result = user.send_email_confirmation_code(email)
        else:
            if hasattr(settings, 'GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION') \
                    and settings.GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION:
                serializer = EmailPreConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = UserSession().send_confirmation_code(serializer.data['email'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)

        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = EmailConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = user.check_email_confirmation_code(serializer.data['email_confirmation_code'])
        else:
            if hasattr(settings, 'GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION') \
                    and settings.GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION:
                serializer = EmailPreConfirmCheckCodeSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = UserSession().check_confirmation_code(serializer.data['email'],
                                                               serializer.data['email_confirmation_code'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)
        return Response(result)
