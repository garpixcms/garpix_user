from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        super(LoginForm, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        valid = False
        if username and password:
            user = User.objects.filter(username=username.lower()).first()

            if not user:
                raise forms.ValidationError(_('User is not found'))

            if user and not user.is_active:
                raise forms.ValidationError(_('User is inactive. You must confirm the registration email address at registration.'))

            valid = user.check_password(password)
        if not valid:
            raise forms.ValidationError(_('Invalid: username / password'))
        return valid
