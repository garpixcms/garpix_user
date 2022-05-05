from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.utils.module_loading import import_string
from gitdb.utils.encoding import force_text
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
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


class EmailLinkConfirmationViewSet(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return EmailConfirmSendSerializer
        return EmailPreConfirmCheckCodeSerializer

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION != 0 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
            try:
                serializer = EmailPreConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                email = request.data['email']
                user = User.objects.filter(email=email).first()
                result = user.send_confirmation_link(email)
            except Exception as e:
                return Response(e, status=401)
        else:
            return Response({'Функция подтверждения пользователя отключена'}, status=401)
        return Response(result)

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION != 0 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
            if user.is_authenticated:
                serializer = EmailConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                email = request.data['email']
                user = User.objects.filter(email=email).first()
                result = user.send_confirmation_link(email)
            else:
                if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION == 1 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
                    serializer = EmailPreConfirmSendSerializer(data=request.data)
                    serializer.is_valid(raise_exception=True)
                    result = User().send_link_email(serializer.data['email'])
                else:
                    return Response({'Учетные данные не были предоставлены'}, status=401)
        else:
            return Response({'Функция подтверждения пользователя отключена'}, status=401)
        return Response(result)

    @api_view(['GET'])
    def activate(self, token, confirmation_code):
        User = get_user_model()
        if GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION == 2 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
            try:
                uid = force_text(urlsafe_base64_decode(token))
                user_info = User.objects.get(pk=uid, email_confirmation_code=confirmation_code)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'Пользователь не подтвержден!'}, status=401)
            if user_info:
                user_info.is_email_confirmed = True
                user_info.save()
                return Response({'Почта подтверждена'}, status=200)
            else:
                return Response({'Пользователь не подтвержден!'}, status=401)
        elif GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION == 1 and settings.GARPIX_USE_REGISTRATION_EMAIL_CONFIRMATION:
            result = User().check_link_email(token=token, email_confirmation_code=confirmation_code)
            return Response(result)
        else:
            return Response({'Подтверждение отключено'}, status=401)

