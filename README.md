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

]
```

For custom auth with phone and email use this in `settings.py`:

```python
# ...

AUTHENTICATION_BACKENDS = (
    # Django
    'garpix_user.utils.backends.CustomAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

```

## With Django Rest Framework

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
        'garpix_auth.rest.authentication.MainAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    }
}

AUTHENTICATION_BACKENDS = (
    # Only your social networks
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Django
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

```

## Email and phone confirmation, password restoring

To use email and phone confirmation or (and) restore password functionality add the `garpix_notify` to your `INSTALLED_APPS`:

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

You also need import email or (and) phone confirmation notify events:

```python
from garpix_user.settings import EMAIL_CONFIRMATION_EVENT, EMAIL_CONFIRMATION_EVENT_ITEM  # noqa
from garpix_user.settings import PHONE_CONFIRMATION_EVENT, PHONE_CONFIRMATION_EVENT_ITEM  # noqa

NOTIFY_EVENTS = {}  # if you haven't any notifications in your project

NOTIFY_EVENTS.update(PHONE_CONFIRMATION_EVENT_ITEM)
NOTIFY_EVENTS.update(EMAIL_CONFIRMATION_EVENT_ITEM)

```

The same notification events to restore password:
```python
from garpix_user.settings import EMAIL_RESTORE_PASSWORD_EVENT, EMAIL_RESTORE_PASSWORD_EVENT_ITEM  # noqa
from garpix_user.settings import PHONE_RESTORE_PASSWORD_EVENT, PHONE_RESTORE_PASSWORD_EVENT_ITEM  # noqa

NOTIFY_EVENTS = {}  # if you haven't any notifications in your project

NOTIFY_EVENTS.update(PHONE_RESTORE_PASSWORD_EVENT_ITEM)
NOTIFY_EVENTS.update(EMAIL_RESTORE_PASSWORD_EVENT_ITEM)

```

You can specify email and phone code length and lifetime:
```python
GARPIX_CONFIRM_CODE_LENGTH = 6
GARPIX_CONFIRM_PHONE_CODE_LIFE_TIME = 5  # in minutes
GARPIX_CONFIRM_EMAIL_CODE_LIFE_TIME = 2  # in days
```

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
    'USE_EMAIL_LINK_CONFIRMATION': True,
    'EMAIL_CONFIRMATION_LINK_REDIRECT': '',  # link to the page user needs to see after email confirmation
}

# Hint: see all available settings in the end of this document.

```

## Referral links

You can also use referral links in your project with garpix_user. To add this functionality, just add the corresponding settings:

```python  

# settings.py

GARPIX_USER = {
    'USE_REFERRAL_LINKS': True,
    'REFERRAL_REDIRECT_URL': '/', # link to the page user needs to see
}

```

## UserSession

Using `garpix_user` you can also store info about unregistered user sessions. The package already consists of model and views for it.

To create the unregistered user send `POST` request to `{API_URL}/user_session/create_user_session/`

The request returns `UserSession` object with `token_number` field. You need to send this token number in each request passing in to header as `UserSession-Token`.


## All available settings

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
    'EMAIL_CONFIRMATION_LINK_REDIRECT': '',
    'CONFIRM_CODE_LENGTH': 6,
    'TIME_LAST_REQUEST': 1,
    'CONFIRM_PHONE_CODE_LIFE_TIME': 5,  # in minutes
    'CONFIRM_EMAIL_CODE_LIFE_TIME': 2,  # in days
    # restore password
    'USE_EMAIL_RESTORE_PASSWORD': True,
    'USE_PHONE_RESTORE_PASSWORD': True,
    # response messages
    'WAIT_RESPONSE': 'Не прошло 1 мин с момента предыдущего запроса',
    'USER_REGISTERED_RESPONSE': 'Пользователь с таким {field} уже зарегистрирован',  # as 'field' will be used email/phone according to the request
    'INCORRECT_CODE_RESPONSE': 'Некорретный код',
    'NO_TIME_LEFT_RESPONSE': 'Код недействителен. Запросите повторно',
    'NOT_AUTHENTICATED_RESPONSE': 'Учетные данные не были предоставлены'
}

```

See `garpix_user/tests/test_api.py` for examples.

# Changelog

See [CHANGELOG.md](backend/garpix_user/CHANGELOG.md).

# Contributing

See [CONTRIBUTING.md](backend/garpix_user/CONTRIBUTING.md).

# License

[MIT](LICENSE)

---

Developed by Garpix / [https://garpix.com](https://garpix.com)