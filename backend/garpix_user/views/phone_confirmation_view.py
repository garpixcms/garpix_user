from django.conf import settings
from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotAuthenticated, ValidationError
from rest_framework.response import Response

from garpix_user.exceptions import NotAuthenticateException
from garpix_user.serializers import PhoneConfirmSendSerializer, PhoneConfirmCheckCodeSerializer, \
    PhonePreConfirmSendSerializer
from garpix_user.models import UserSession
from django.utils.translation import ugettext as _

from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class PhoneConfirmationView(viewsets.GenericViewSet):

    def get_serializer_class(self):
        user = self.request.user
        if self.action == 'send_code':
            if user.is_authenticated:
                return PhoneConfirmSendSerializer
            return PhonePreConfirmSendSerializer
        if self.action == 'check_code':
            return PhoneConfirmCheckCodeSerializer
        return PhoneConfirmCheckCodeSerializer

    @extend_schema(summary=_('Phone confirmation. Step 1'))
    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            result = user.send_phone_confirmation_code(serializer.data.get('phone', None))
            if result is not True:
                result.raise_exception(exception_class=ValidationError)
            return Response({'result': 'success'})
        else:
            if settings.GARPIX_USER.get('USE_PREREGISTRATION_PHONE_CONFIRMATION', False):
                user = UserSession.get_or_create_user_session(request)
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                result = user.send_phone_confirmation_code(serializer.data['phone'])
                if result is not True:
                    result.raise_exception(exception_class=ValidationError)
                return Response({'result': 'success'})

            raise NotAuthenticateException().raise_exception(exception_class=NotAuthenticated)

    @extend_schema(summary=_('Phone confirmation. Step 2'))
    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            if settings.GARPIX_USER.get('USE_PREREGISTRATION_PHONE_CONFIRMATION', False):
                user = UserSession.get_or_create_user_session(request)
            else:
                raise NotAuthenticateException().raise_exception(exception_class=NotAuthenticated)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = user.confirm_phone(serializer.data['phone_confirmation_code'])
        if result is not True:
            result.raise_exception(exception_class=ValidationError)
        return Response({'result': 'success'})
