# Garpix User

Auth module for Django/DRF projects. Part of GarpixCMS.

Used packages:

* [django rest framework](https://www.django-rest-framework.org/api-guide/authentication/)
* [social-auth-app-django](https://github.com/python-social-auth/social-app-django)
* [django-rest-framework-social-oauth2](https://github.com/RealmTeam/django-rest-framework-social-oauth2)
* etc; see setup.py

## Quickstart

Install with pip:

```bash
pip install garpix_user
```

Add the `garpix_user` to your `INSTALLED_APPS`:

```python
# settings.py

# ...
INSTALLED_APPS = [
    # ...
    'garpix_user',
]
```

and to migration modules:

```python
# settings.py

# ...
MIGRATION_MODULES = {
    'garpix_user': 'app.migrations.garpix_user',
}
```

Add to `urls.py`:

```python
from garpix_user.views import LogoutView, LoginView

# ...
urlpatterns = [
    # ...
    # garpix_user
    path('', include(('garpix_user.urls', 'user'), namespace='garpix_user')),
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="authorize"),
]
```

Use `GarpixUser` from `garpix_user.models` as base for your user model class:

```python
# user.models.user.py

from garpix_user.models import GarpixUser


class User(GarpixUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

```

Use `UserAdmin` from `garpix_user.admin` as base for your user admin class:

```python

from django.contrib import admin

from garpix_user.admin import UserAdmin
from user.models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    pass

```

For custom auth with phone and/or email use this in `settings.py`:

```python
# ...

AUTHENTICATION_BACKENDS = (
    # Django
    'garpix_user.utils.backends.CustomAuthenticationBackend'
)

```

and `USERNAME_FIELDS` to your `User` model:

```python
# user.models.user.py

from garpix_user.models import GarpixUser


class User(GarpixUser):
    USERNAME_FIELDS = ('email',)  # default is username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

```

## With Django Rest Framework

Import settings from `garpix_user`:

```python
# settings.py
from garpix_user.settings import *

```

Add this for SPA:

```python
# ...
INSTALLED_APPS += [
    # ...
    'rest_framework',
    'rest_framework.authtoken',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    # ...
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': {
        'garpix_user.rest.authentication.MainAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    }
}

```

### JWT Token

You can use JWT token. To do it set `REST_AUTH_TOKEN_JWT` settings to True. You also need to
set `JWT_SECRET_KEY`, `JWT_SERIALIZER` settings:

```python
# settings.py

# ...

GARPIX_USER = {
    'REST_AUTH_TOKEN_JWT': True,
    'JWT_SECRET_KEY': env('JWT_SECRET_KEY'),  # secret code to validate JWT token
    'JWT_SERIALIZER': 'garpix_user.serializers.JWTDataSerializer'
}

# Hint: see all available settings in the end of this document.

```

### Authorization headers

You can override the Bearer authorization header by `REST_AUTH_HEADER_KEY` setting.
And also allow this custom header for cors-headers:

```python
# settings.py

# ...
from corsheaders.defaults import default_headers

GARPIX_USER = {
    'REST_AUTH_HEADER_KEY': 'HTTP_BEARER_AUTHORIZATION'
}

# Hint: see all available settings in the end of this document.

CORS_ALLOW_HEADERS = list(default_headers) + [
    "Bearer-Authorization",
]
```

Now you need to add `Bearer-Authorization` header instead of `Authorization` header with your Bearer token to all
requests.

## Registration

`garpix_user` adds default registration for with `phone` and/or `email` and `password` fields. To add fields to this
form override `RegistrationSerializer` and add it to `settings`:

```python
# settings.py

GARPIX_USER = {
    # registration
    'REGISTRATION_SERIALIZER': 'app.serializers.RegistrationCustSerializer'
}

# Hint: see all available settings in the end of this document.

```

```python
# app.serializers.py

from django.contrib.auth import get_user_model
from rest_framework import serializers

from garpix_user.serializers import RegistrationSerializer

User = get_user_model()


class RegistrationCustSerializer(RegistrationSerializer):
    extra_field = serializers.CharField(write_only=True)

    class Meta(RegistrationSerializer.Meta):
        model = User
        fields = RegistrationSerializer.Meta.fields + ('extra_field',)

```

You also can add password security settings:

```python

# settings.py

GARPIX_USER = {
    # registration
    'MIN_LENGTH_PASSWORD': 8,
    'MIN_DIGITS_PASSWORD': 2,
    'MIN_CHARS_PASSWORD': 2,
    'MIN_UPPERCASE_PASSWORD': 1,
}

# Hint: see all available settings in the end of this document.

```

## Email and phone confirmation, password restoring

To use email and phone confirmation or (and) restore password functionality add the `garpix_notify` to
your `INSTALLED_APPS`:

```python
# settings.py

# ...
INSTALLED_APPS = [
    # ...
    'garpix_notify',
]
```

and to migration modules:

```python
# settings.py

MIGRATION_MODULES = {
    'garpix_notify': 'app.migrations.garpix_notify',
}
```

Add corresponding settings:

```python

# settings.py

GARPIX_USER = {
    'USE_EMAIL_CONFIRMATION': True,
    'USE_PHONE_CONFIRMATION': True,
    'USE_EMAIL_RESTORE_PASSWORD': True,
    'USE_PHONE_RESTORE_PASSWORD': True,
}

# Hint: see all available settings in the end of this document.

```

You also need to add notify events:

```python
# settings.py

NOTIFY_EVENTS.update(GARPIX_USER_NOTIFY_EVENTS)

```

You can specify email and phone code length, lifetime, confirmation lifetime and time delay before next attempt:

```python
# settings.py 

GARPIX_USER = {
    'CONFIRM_PHONE_CODE_LENGTH': 6,
    'CONFIRM_EMAIL_CODE_LENGTH': 6,
    'TIME_LAST_REQUEST': 1,
    'CONFIRM_PHONE_CODE_LIFE_TIME': 5,  # in minutes
    'CONFIRM_EMAIL_CODE_LIFE_TIME': 2,
    'CONFIRM_EMAIL_CODE_LIFE_TIME_TYPE': 'days', # available types are: ['days', 'minutes'], default is 'days'
    'PHONE_CONFIRMATION_LIFE_TIME': 2,  # in days
    'EMAIL_CONFIRMATION_LIFE_TIME': 2,  # in days
}

# Hint: see all available settings in the end of this document.

```

Notice: the minimum and maximum values for `CONFIRM_CODE_LENGTH` are 4 and 255. These values will be hard used in case
your settings are not in this interval.

If you need to use pre-registration email or phone confirmation, you need to set corresponding variables to True:

```python

# settings.py

GARPIX_USER = {
    'USE_PREREGISTRATION_EMAIL_CONFIRMATION': True,
    'USE_PREREGISTRATION_PHONE_CONFIRMATION': True,
}

# Hint: see all available settings in the end of this document.

```

If you need to use email confirmation by link, you need to set corresponding variable:

```python

# settings.py

GARPIX_USER = {
    'USE_EMAIL_LINK_CONFIRMATION': True
}

# Hint: see all available settings in the end of this document.

```

You can also override `confirm_link_redirect_url` method of `User` model to form confirmation link as you need.

By default, users with unconfirmed email/phone number will be deleted in 10 days. You can set up it
using `CONFIRMATION_DELAY`:

```python
# settings.py

GARPIX_USER = {
    # ...
    'CONFIRMATION_DELAY': 10,  # in days
}
# Hint: see all available settings in the end of this document.

```

## Referral links

You can also use referral links in your project with garpix_user. To add this functionality, just add the corresponding
settings:

```python  

# settings.py

GARPIX_USER = {
    'USE_REFERRAL_LINKS': True,
    'REFERRAL_REDIRECT_URL': '/', # link to the page user needs to see
}
# Hint: see all available settings in the end of this document.

```

## UserSession

Using `garpix_user` you can also store info about unregistered user sessions. The package already consists of model and
views for it.

To create the unregistered user send `POST` request to `{API_URL}/user_session/create_user_session/`

The request returns `UserSession` object with `token_number` field. You need to send this token number in each request
passing in to header as `user-session-token`.

By default, on log in current user session instance will be dropped, if system has `registered` user session instance
for authorized user. You can override `set_user_session` method of `User` model to add custom logic.

## All available settings with default values

```python

# settings.py

GARPIX_USER = {
    # base settings
    'USE_REFERRAL_LINKS': False,
    'REFERRAL_REDIRECT_URL': '/',
    # email/phone confirmation
    'USE_EMAIL_CONFIRMATION': True,
    'USE_PHONE_CONFIRMATION': True,
    'USE_PREREGISTRATION_EMAIL_CONFIRMATION': True,
    'USE_PREREGISTRATION_PHONE_CONFIRMATION': True,
    'USE_EMAIL_LINK_CONFIRMATION': True,
    'CONFIRM_PHONE_CODE_LENGTH': 6,
    'CONFIRM_EMAIL_CODE_LENGTH': 6,
    'TIME_LAST_REQUEST': 1,
    'CONFIRM_PHONE_CODE_LIFE_TIME': 5,  # in minutes
    'CONFIRM_EMAIL_CODE_LIFE_TIME': 2,
    'CONFIRM_EMAIL_CODE_LIFE_TIME_TYPE': 'days', # available types are: ['days', 'minutes'], default is 'days'
    'PHONE_CONFIRMATION_LIFE_TIME': 2,  # in days
    'EMAIL_CONFIRMATION_LIFE_TIME': 2,  # in days
    'CONFIRMATION_DELAY': 10,  # in days
    # restore password
    'USE_RESTORE_PASSWORD': True,
    # registration
    'USE_REGISTRATION': True,
    'REGISTRATION_SERIALIZER': 'app.serializers.RegistrationCustSerializer',
    'MIN_LENGTH_PASSWORD': 8,
    'MIN_DIGITS_PASSWORD': 2,
    'MIN_CHARS_PASSWORD': 2,
    'MIN_UPPERCASE_PASSWORD': 1,
    # authorizations
    'REST_AUTH_HEADER_KEY': 'HTTP_AUTHORIZATION',
    'REST_AUTH_TOKEN_JWT': False,
    'JWT_SERIALIZER': 'garpix_user.serializers.JWTDataSerializer',
    # response messages
    'WAIT_RESPONSE': 'Не прошло 1 мин с момента предыдущего запроса',
    'USER_REGISTERED_RESPONSE': 'Пользователь с таким {field} уже зарегистрирован',
    # as 'field' will be used email/phone according to the request
    'INCORRECT_CODE_RESPONSE': 'Некорретный код',
    'NO_TIME_LEFT_RESPONSE': 'Код недействителен. Запросите повторно',
    'NOT_AUTHENTICATED_RESPONSE': 'Учетные данные не были предоставлены'
}

```

See `garpix_user/tests/test_api/*.py` for examples.



# For Frontend Developers

UserSession - needed to associate an unauthorized user with other entities in our system.

To create a UserSession, you need to call the method:

`/api/garpix_user/user_session/create_user_session/`

Next, you need to put it in a cookie or other storage and pass it in a special header. UserSession-Token.

## Phone Verification

Happens in two steps

1. Send `/api/garpix_user/confirm_phone/send_code/` in the request body send the **phone.** field The phone number will
   be saved and a confirmation code will be sent to it.
2. After that, you need to send the code `/api/garpix_user/confirm_phone/check_code/` in the field **
   phone_confirmation_code**

If everything went well, the phone will be confirmed

# Changelog

See [CHANGELOG.md](CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)