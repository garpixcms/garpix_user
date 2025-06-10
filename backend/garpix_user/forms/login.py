from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from datetime import timedelta

from garpix_utils.cef_logs.event import LoginEvent, LoginFailedEvent

from garpix_user.utils.current_date import set_current_date
from garpix_user.utils.get_password_settings import get_password_settings

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):

        password_validity_period = get_password_settings()['password_validity_period']

        super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        valid = False
        if username and password:
            user = User.objects.filter(username=username.lower()).first()

            if not user or user.keycloak_auth_only:
                raise forms.ValidationError(_('User is not found'))

            if user and not user.is_active:
                raise forms.ValidationError(_('User is inactive. You must confirm the registration email address at registration.'))

            valid = user.check_password(password)

            if not valid:
                raise forms.ValidationError(_('Invalid: username / password'))

            message = f'Неудачная попытка входа. Пользователь {user.username}.'
            event = LoginFailedEvent()

            if user and user.is_blocked:
                event(request=self.request, user=user, msg=message)
                raise forms.ValidationError(_("Your account is blocked. Please contact your administrator"))
            if user and password_validity_period != -1 and not user.keycloak_auth_only and user.password_updated_date + timedelta(
                    days=password_validity_period) <= set_current_date():
                event(request=self.request, user=user, msg=message)
                raise forms.ValidationError(_('Your password has expired. Please change password'))

            message = f'Пользователь {user.username} вошел в систему.'

            LoginEvent()(request=self.request, user=user, msg=message)

        return valid
