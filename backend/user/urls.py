from django.urls import path, re_path
from rest_framework import routers
from garpix_user.urls import urlpatterns
from garpix_user.views.registration_view import registration_view
from garpix_user.views.user_session_view import UserSessionView

from garpix_user.views import EmailConfirmationView, PhoneConfirmationView, RestoreEmailPasswordView, \
    RestorePhonePasswordView, EmailConfirmationLinkView

urlpatterns += [
    path('registration/', registration_view, name='registration'),
    re_path(r'hash/^(?P<hash>.*?)/$', EmailConfirmationLinkView.as_view(), name='email_confirmation_link'),
    re_path(r'hash/^(?P<hash>.*?)$', EmailConfirmationLinkView.as_view(), name='email_confirmation_link')
]
router = routers.DefaultRouter()
router.register(r'user_session', UserSessionView, basename='api_user_session')
router.register(r'confirm_email', EmailConfirmationView, basename='api_confirm_email')
router.register(r'confirm_phone', PhoneConfirmationView, basename='api_confirm_phone')
router.register(r'restore_email_password', RestoreEmailPasswordView, basename='api_restore_email_password')
router.register(r'restore_phone_password', RestorePhonePasswordView, basename='api_restore_phone_password')
urlpatterns += router.urls
