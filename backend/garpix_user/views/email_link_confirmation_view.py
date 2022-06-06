from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from gitdb.utils.encoding import force_text
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from garpix_user import settings
from garpix_user.serializers import EmailConfirmSendSerializer, EmailConfirmCheckCodeSerializer
from garpix_user.models import UserSession

User = get_user_model()


class EmailLinkConfirmationView(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return EmailConfirmSendSerializer
        if self.action == 'check_code':
            return EmailConfirmCheckCodeSerializer
        return EmailConfirmSendSerializer

    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = EmailConfirmSendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = request.data['email']
            user = User.objects.filter(email=email).first()
            result = user.send_confirmation_link(email)
        else:
            if hasattr(settings, 'GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION') \
                    and settings.GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION:
                serializer = EmailPreConfirmSendSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                result = User().send_link_email(serializer.data['email'])
            else:
                return Response({'Учетные данные не были предоставлены'}, status=401)

        return Response(result)

    @api_view(['GET'])
    def activate(self, token, confirmation_code):
        User = get_user_model()
        if hasattr(settings, 'GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION') \
                and settings.GARPIX_USE_PREREGISTRATION_EMAIL_CONFIRMATION:
            result = UserSession().check_link_email(token=token, email_confirmation_code=confirmation_code)
            return Response(result)
        else:
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
