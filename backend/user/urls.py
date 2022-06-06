from django.urls import path
from rest_framework import routers
from garpix_user.urls import urlpatterns
from garpix_user.views.registration_views import registration_view
from garpix_user.views.user_session import UserSessionView

from garpix_user.views import EmailConfirmationView, PhoneConfirmationView, RestoreEmailPasswordView, \
    RestorePhonePasswordView

urlpatterns += [
    path('registration/', registration_view, name='registration')
]
router = routers.DefaultRouter()
router.register(r'user_session', UserSessionView, basename='api_user_session')
router.register(r'confirm_email', EmailConfirmationView, basename='api_confirm_email')
router.register(r'confirm_phone', PhoneConfirmationView, basename='api_confirm_phone')
router.register(r'restore_email_password', RestoreEmailPasswordView, basename='api_restore_email_password')
router.register(r'restore_phone_password', RestorePhonePasswordView, basename='api_restore_phone_password')
urlpatterns += router.urls
