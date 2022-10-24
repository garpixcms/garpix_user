from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from garpix_user.exceptions import ValidationErrorSerializer
from garpix_user.models import UserSession
from garpix_user.serializers import RestoreByPhoneSerializer, UserSessionTokenSerializer
from garpix_user.serializers.restore_passwrod_serializer import RestoreCheckCodeSerializer, RestoreSetPasswordSerializer
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class RestorePhonePasswordView(viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'send_code':
            return RestoreByPhoneSerializer
        if self.action == 'check_code':
            return RestoreCheckCodeSerializer
        return RestoreSetPasswordSerializer

    @extend_schema(
        summary='Restore password by phone. Step 1',
        responses={
            status.HTTP_200_OK: UserSessionTokenSerializer,
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer
        }
    )
    @action(methods=['POST'], detail=False)
    def send_code(self, request, *args, **kwargs):
        user = UserSession.get_or_create_user_session(request)
        serializer = RestoreByPhoneSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result, error = user.send_restore_code(phone=serializer.data['phone'])

        if not result:
            result.raise_exception(exception_class=ValidationError)
        return Response(UserSessionTokenSerializer(user).data)

    @extend_schema(
        summary='Restore password by phone. Step 2',
        responses={
            status.HTTP_204_NO_CONTENT: '',
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer
        }
    )
    @action(methods=['POST'], detail=False)
    def check_code(self, request, *args, **kwargs):
        user = UserSession.get_or_create_user_session(request)

        serializer = RestoreCheckCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result, error = user.check_restore_code(restore_confirmation_code=serializer.data['restore_confirmation_code'])

        if not result:
            result.raise_exception(exception_class=ValidationError)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary='Restore password by phone. Step 3',
        responses={
            status.HTTP_200_OK: _('Password was updated!'),
            status.HTTP_400_BAD_REQUEST: ValidationErrorSerializer
        }
    )
    @action(methods=['POST'], detail=False)
    def set_password(self, request, *args, **kwargs):
        user = UserSession.get_or_create_user_session(request)

        serializer = RestoreSetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result, error = user.restore_password(field='phone', new_password=serializer.data['new_password'])

        if not result:
            result.raise_exception(exception_class=ValidationError)
        return Response(_('Password was updated!'))
