import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, HttpResponseGone
from django.views.generic import RedirectView

from garpix_user.serializers import EmailConfirmSendSerializer, EmailConfirmCheckCodeSerializer, \
    EmailPreConfirmSendSerializer, UserSessionTokenSerializer

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotAuthenticated, ValidationError
from garpix_user.models import UserSession
from django.utils.translation import ugettext as _

from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class EmailConfirmationView(viewsets.GenericViewSet):

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'send_code':
            if user.is_authenticated:
                return EmailConfirmSendSerializer
            return EmailPreConfirmSendSerializer
        return EmailConfirmCheckCodeSerializer

    @extend_schema(summary=_('Email confirmation. Step 1' if not settings.GARPIX_USER.get('USE_EMAIL_LINK_CONFIRMATION',
                                                                                          False) else 'Send email confirmation link'))
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

    if not settings.GARPIX_USER.get('USE_EMAIL_LINK_CONFIRMATION', True):
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


class EmailConfirmationLinkView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        User = get_user_model()
        hash = self.kwargs.get('hash', None)
        result = User.confirm_email_by_link(hash)
        if result is not True:
            return f"{settings.GARPIX_USER.get('EMAIL_CONFIRMATION_LINK_REDIRECT', '/')}?status=error"
        return f"{settings.GARPIX_USER.get('EMAIL_CONFIRMATION_LINK_REDIRECT', '/')}?status=success"
