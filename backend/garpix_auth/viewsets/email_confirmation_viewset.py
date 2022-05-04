from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth import settings
from garpix_auth.serializers import EmailConfirmSendSerializer, EmailConfirmCheckCodeSerializer, \
    EmailPreConfirmCheckCodeSerializer, EmailPreConfirmSendSerializer

User = get_user_model()

try:
    Config = import_string(settings.GARPIX_USER_CONFIG)
    GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION = Config.get_solo().registration_type
except Exception:
    GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION = getattr(settings, 'GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION', 2)


class EmailConfirmationViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return EmailConfirmSendSerializer
        return EmailPreConfirmCheckCodeSerializer

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION != 0 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
            if user.is_authenticated:
                serializer = EmailConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                email = request.data('email', None)
                result = user.send_email_confirmation_code(email)
            else:
                if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION == 1 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
                    serializer = EmailPreConfirmSendSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    result = User().send_confirmation_code(serializer.data['email'])
                else:
                    return Response({'Учетные данные не были предоставлены'}, status=401)
        else:
            return Response({'Функция подтверждения пользователя отключена'}, status=401)
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = EmailConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = user.check_email_confirmation_code(serializer.data['email_confirmation_code'])
        else:
            if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION == 1 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
                serializer = EmailPreConfirmCheckCodeSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = User().check_confirmation_code(serializer.data['email'],
                                                        serializer.data['email_confirmation_code'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)
        return Response(result)
