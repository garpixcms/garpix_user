from datetime import timedelta

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authentication import authenticate

from garpix_user.utils.current_date import set_current_date
from garpix_user.utils.get_password_settings import get_password_settings


class AuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        username = username.lower()

        if username and password:
            password_validity_period = get_password_settings()['password_validity_period']

            request = self.context.get('request')
            user = authenticate(request=request,
                                username=username, password=password)
            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user or user.keycloak_auth_only:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if user.is_blocked:
                msg = _(
                    'Your account is blocked. Please contact your administrator')
                raise serializers.ValidationError(msg, code='authorization')

            if password_validity_period != -1 and not user.keycloak_auth_only and user.password_updated_date + timedelta(
                    days=password_validity_period) <= set_current_date():
                msg = {
                    'non_field_errors': [
                        _('Your password has expired. Please change password')],
                    'extra_parameters': ['needs_password_update']
                }
                raise serializers.ValidationError(msg, code='authorization')

            if user.needs_password_update:
                msg = {
                    'non_field_errors': [
                        _('Your need to reset your password to activate your account')],
                    'extra_parameters': ['needs_password_update']
                }
                raise serializers.ValidationError(msg, code='authorization')

            user.set_user_session(request)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
