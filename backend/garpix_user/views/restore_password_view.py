from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from garpix_user.models import UserSession
from garpix_user.serializers import RestorePasswordSerializer, UserSessionTokenSerializer
from garpix_user.serializers.restore_passwrod_serializer import RestoreCheckCodeSerializer, RestoreSetPasswordSerializer
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class RestorePasswordView(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return RestorePasswordSerializer
        if self.action == 'check_code':
            return RestoreCheckCodeSerializer
        return RestoreSetPasswordSerializer

    @extend_schema(summary=_('Restore password. Step 1'))
    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserSession.get_or_create_user_session(request, username=serializer.data['username'])

        result, error = user.send_restore_code(username=serializer.data['username'])

        if not result:
            error.raise_exception(exception_class=ValidationError)
        return Response(UserSessionTokenSerializer(user).data)

    @extend_schema(summary=_('Restore password. Step 2'))
    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = UserSession.get_or_create_user_session(request)

        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        result, error = user.check_restore_code(
            restore_password_confirm_code=serializer.data['restore_password_confirm_code'])
        if not result:
            error.raise_exception(exception_class=ValidationError)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(summary=_('Restore password. Step 3'))
    @action(methods=['POST'], detail=False)
    def set_password(self, request, *args, **kwargs):
        user = UserSession.get_or_create_user_session(request)

        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        result, error = user.restore_password(field='username', new_password=serializer.data['new_password'])

        if not result:
            error.raise_exception(exception_class=ValidationError)
        return Response({"result": _('Password was updated!')})
