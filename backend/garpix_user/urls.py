from django.conf import settings
from django.urls import path, re_path, include
from garpix_user.views import obtain_auth_token, refresh_token_view, logout_view, ChangePasswordView
from rest_framework import routers
from garpix_user.views.user_session_view import UserSessionView
from garpix_user.views.registration_view import registration_view
from garpix_user.views.referral_links_view import ReferralLinkView

from django.contrib import admin
from .forms import LoginForm

admin.autodiscover()
admin.site.login_form = LoginForm

from garpix_user.views import (
    EmailConfirmationView, PhoneConfirmationView,
    RestorePasswordView,
    EmailConfirmationLinkView
)

app_name = 'garpix_user'

GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())

# api routing

router = routers.DefaultRouter()

router.register(r'user_session', UserSessionView, basename='api_user_session')
router.register('', ChangePasswordView, basename='api_change_password')

if GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False):
    router.register(r'confirm_email', EmailConfirmationView, basename='api_confirm_email')
if GARPIX_USER_SETTINGS.get('USE_PHONE_CONFIRMATION', False):
    router.register(r'confirm_phone', PhoneConfirmationView, basename='api_confirm_phone')
if GARPIX_USER_SETTINGS.get('USE_RESTORE_PASSWORD', False):
    router.register(r'restore_password', RestorePasswordView, basename='api_restore_password')

api_urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout'),
    path(r'', include(router.urls))
]

urlpatterns = [
    path(f'{settings.API_URL}/garpix_user/', include((api_urlpatterns, 'garpix_user'), namespace='garpix_user_api')),
]

if GARPIX_USER_SETTINGS.get('USE_REGISTRATIONS', True):
    api_urlpatterns.append(path('register/', registration_view, name='api_registration'))

if GARPIX_USER_SETTINGS.get('USE_REFERRAL_LINKS', False):
    urlpatterns += [
        re_path(r'invite_link/(?P<hash>.*?)/$', ReferralLinkView.as_view(), name='referral_link'),
        re_path(r'invite_link/(?P<hash>.*?)$', ReferralLinkView.as_view(), name='referral_link')
    ]

if GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get('USE_EMAIL_LINK_CONFIRMATION',
                                                                                          True):
    urlpatterns += [
        re_path(r'confirm_email/(?P<model_type>.*?)/(?P<hash>.*?)/$', EmailConfirmationLinkView.as_view(),
                name='email_confirmation_link'),
        re_path(r'confirm_email/(?P<model_type>.*?)/(?P<hash>.*?)$', EmailConfirmationLinkView.as_view(),
                name='email_confirmation_link'),
    ]
