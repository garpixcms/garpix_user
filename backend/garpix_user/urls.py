from django.conf import settings
from django.urls import path, re_path, include
from garpix_user.views import obtain_auth_token, refresh_token_view, logout_view
from rest_framework import routers
from garpix_user.views.user_session_view import UserSessionView
from garpix_user.views.registration_view import registration_view
from garpix_user.views.referral_links_view import ReferralLinkView
from garpix_user.views.login_views import LogoutView, LoginView

from garpix_user.views import (
    EmailConfirmationView, PhoneConfirmationView,
    RestoreEmailPasswordView, RestorePhonePasswordView,
    EmailConfirmationLinkView
)

GARPIX_USER_SETTINGS = getattr(settings, 'GARPIX_USER', dict())

# api routing

api_urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout'),
    path('register/', registration_view, name='api_registration')
]

router = routers.DefaultRouter()

router.register(r'user_session', UserSessionView, basename='api_user_session')

if GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False):
    router.register(r'confirm_email', EmailConfirmationView, basename='api_confirm_email')
if GARPIX_USER_SETTINGS.get('USE_PHONE_CONFIRMATION', False):
    router.register(r'confirm_phone', PhoneConfirmationView, basename='api_confirm_phone')
if GARPIX_USER_SETTINGS.get('USE_EMAIL_RESTORE_PASSWORD', False):
    router.register(r'restore_email_password', RestoreEmailPasswordView, basename='api_restore_email_password')
if GARPIX_USER_SETTINGS.get('USE_PHONE_RESTORE_PASSWORD', False):
    router.register(r'restore_phone_password', RestorePhonePasswordView, basename='api_restore_phone_password')

api_urlpatterns += router.urls

urlpatterns = [
    path(f'{settings.API_URL}/garpix_user/', include((api_urlpatterns, 'garpix_user'), namespace='garpix_user_api')),
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="authorize"),
]

if GARPIX_USER_SETTINGS.get('USE_REFERRAL_LINKS', False):
    urlpatterns += [
        re_path(r'hash/^(?P<hash>.*?)/$', ReferralLinkView.as_view(), name='referral_link'),
        re_path(r'hash/^(?P<hash>.*?)$', ReferralLinkView.as_view(), name='referral_link')
    ]

if GARPIX_USER_SETTINGS.get('USE_EMAIL_CONFIRMATION', False) and GARPIX_USER_SETTINGS.get('USE_EMAIL_LINK_CONFIRMATION',
                                                                                          False):
    urlpatterns += [
        re_path(r'confirm_email/hash/^(?P<hash>.*?)/$', EmailConfirmationLinkView.as_view(),
                name='email_confirmation_link'),
        re_path(r'confirm_email/hash/^(?P<hash>.*?)$', EmailConfirmationLinkView.as_view(),
                name='email_confirmation_link'),
    ]
