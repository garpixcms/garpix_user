from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_auth.serializers import (PhoneConfirmSendSerializer, PhoneConfirmCheckCodeSerializer, \
                                     PhonePreConfirmCheckCodeSerializer, PhonePreConfirmSendSerializer)

User = get_user_model()

try:
    Config = import_string(settings.GARPIX_USER_CONFIG)
    GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION = Config.get_solo().registration_type
except Exception:
    GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION = getattr(settings, 'GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION', 2)


class PhoneConfirmationViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return PhoneConfirmSendSerializer
        return PhonePreConfirmCheckCodeSerializer

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION != 0 and settings.GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION:
            if user.is_authenticated:
                serializer = PhoneConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                phone = request.data('phone', None)
                result = user.send_phone_confirmation_code(phone)
            else:
                if GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION == 1 and settings.GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION:
                    serializer = PhonePreConfirmSendSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    result = User().send_confirmation_code(serializer.data['phone'])
                else:
                    return Response({'Учетные данные не были предоставлены'}, status=401)
        else:
            return Response({'Функция подтверждения пользователя отключена'}, status=401)
        return Response(result)

    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = PhoneConfirmCheckCodeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            result = user.check_phone_confirmation_code(serializer.data['phone_confirmation_code'])
        else:
            if GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION == 1 and settings.GARPIX_USE_REGISTRATION_PHONE_CONFIRMATION:
                serializer = PhonePreConfirmCheckCodeSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = User().check_confirmation_code(serializer.data['phone'],
                                                                serializer.data['phone_confirmation_code'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)
        return Response(result)
