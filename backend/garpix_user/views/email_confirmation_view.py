from django.conf import settings
from garpix_user.exceptions import NotAuthenticateException
from garpix_user.serializers import EmailConfirmSendSerializer, EmailConfirmCheckCodeSerializer, \
    EmailPreConfirmSendSerializer, UserSessionTokenSerializer

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, ValidationError
from garpix_user.models import UserSession
from django.utils.translation import ugettext as _


class EmailConfirmationView(viewsets.GenericViewSet):

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'send_code':
            if user.is_authenticated:
                return EmailConfirmSendSerializer
            return EmailPreConfirmSendSerializer
        if self.action == 'check_code':
            return EmailConfirmCheckCodeSerializer
        if self.action == 'check_link':
            return EmailConfirmCheckLinkSerializer
        return EmailConfirmSendSerializer

    @extend_schema(summary=_('Email confirmation. Step 1'))
    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = user.send_email_confirmation_code(serializer.data.get('email', None))
            if result is not True:
                result.raise_exception(exception_class=ValidationError)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            if settings.GARPIX_USER.get('USE_PREREGISTRATION_EMAIL_CONFIRMATION', False):
                user = UserSession.get_or_create_user_session(request)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                result = user.send_email_confirmation_code(serializer.data['email'])
                if result is not True:
                    result.raise_exception(exception_class=ValidationError)
                return Response(UserSessionTokenSerializer(user).data)

            raise NotAuthenticated()

    @extend_schema(summary=_('Email confirmation. Step 2'))
    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            if settings.GARPIX_USER.get('USE_PREREGISTRATION_EMAIL_CONFIRMATION', False):
                user = UserSession.get_or_create_user_session(request)
            else:
                raise NotAuthenticated()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = user.confirm_email(serializer.data['email_confirmation_code'])
        if result is not True:
            result.raise_exception(exception_class=ValidationError)
        return Response(status=status.HTTP_204_NO_CONTENT)

    if settings.GARPIX_USER.get('EMAIL_CONFIRM_LINK', None) is not None:
        @extend_schema(summary=_('Email confirmation by link. Step 1'))
        @action(methods=['POST'], detail=False)
        def send_link(self, request, *args, **kwargs):
            serializer_context = super().get_serializer_context()
            user = request.user
            if user.is_authenticated:
                serializer_context.update({'user': user})
                serializer = self.get_serializer(data=request.data, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                user.send_email_confirmation_code(serializer.data.get('email', None))
                return Response(True)
            else:
                if getattr(settings, 'USE_PREREGISTRATION_EMAIL_CONFIRMATION', False):
                    user = UserSession.get_or_create_user_session(request)
                    serializer_context.update({'user': user})
                    serializer = self.get_serializer(data=request.data, context=serializer_context)
                    serializer.is_valid(raise_exception=True)
                    user.send_email_confirmation_code(serializer.data['email'])
                    return Response(EmailPreConfirmSendCodeAnswer(user).data)

                raise NotAuthenticateException().raise_exception(exception_class=NotAuthenticated)

        @extend_schema(summary=_('Email confirmation by link. Step 2'))
        @action(methods=['POST'], detail=False)
        def check_link(self, request, *args, **kwargs):
            serializer_context = super().get_serializer_context()
            serializer = self.get_serializer(data=request.data, context=serializer_context)
            serializer.is_valid(raise_exception=True)
            user.confirm_email()
            return Response(True)
