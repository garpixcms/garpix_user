from django.conf import settings
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from garpix_user.mixins.views.auth_token_mixin import AuthTokenViewMixin
from garpix_user.models import PasswordHistory
from garpix_user.permissions import IsUnAuthenticated
from garpix_user.serializers import ChangePasswordSerializer
from garpix_user.serializers.passwrod_serializer import ChangePasswordUnauthorizedSerializer
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter
from garpix_user.utils.get_password_settings import get_password_settings


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class ChangePasswordView(AuthTokenViewMixin, viewsets.ViewSet):

    def get_serializer_class(self):
        if self.action == 'change_password_unauthorized':
            return ChangePasswordUnauthorizedSerializer
        return ChangePasswordSerializer

    permission_classes = [IsAuthenticated]

    @extend_schema(summary=_('Change password (for authorized users)'))
    @action(methods=['POST'], detail=False)
    def change_password(self, request, *args, **kwargs):

        user = request.user

        if user.keycloak_auth_only:
            return Response({"new_password": [_('You can not change your password. Please contact administrator')]},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer_class()(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        password_history = get_password_settings()['password_history']
        if password_history != -1:
            password_history_rows = PasswordHistory.objects.filter(user=user).order_by(
                '-created_at')[:password_history + 1].values_list('password', flat=True)
            for _pass in password_history_rows:
                if check_password(request.data['new_password'], _pass):
                    return Response({"new_password": [_('You can not use the same password you already had to')]},
                                    status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['new_password'])
        user.save()

        return Response({"result": "success"})

    @extend_schema(summary=_('Change password (for unauthorized users)'))
    @action(methods=['POST'], detail=False, permission_classes=[IsUnAuthenticated])
    def change_password_unauthorized(self, request, *args, **kwargs):

        serializer = self.get_serializer_class()(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        if user.keycloak_auth_only:
            return Response({"new_password": [_('You can not change your password. Please contact administrator')]},
                            status=status.HTTP_400_BAD_REQUEST)

        password_history = get_password_settings()['password_history']
        if password_history != -1:
            password_history_rows = PasswordHistory.objects.filter(user=user).order_by(
                '-created_at')[:password_history + 1].values_list('password', flat=True)
            for _pass in password_history_rows:
                if check_password(request.data['new_password'], _pass):
                    return Response({"new_password": [_('You can not use the same password you already had to')]},
                                    status=status.HTTP_400_BAD_REQUEST)
        user.set_password(request.data['new_password'])
        user.needs_password_update = False
        user.save()

        use_jwt = settings.GARPIX_USER.get('REST_AUTH_TOKEN_JWT', False)

        if use_jwt:
            return self._get_jwt_data(user)
        return self._get_access_token_data(user)
