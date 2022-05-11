from django.urls import path, re_path
from rest_framework import routers

from garpix_auth.views import RegistrationView, obtain_auth_token, refresh_token_view, logout_view

from garpix_auth.viewsets import EmailConfirmationViewSet, PhoneConfirmationViewSet, RestoreEmailPasswordViewSet, \
    EmailConfirmationViewSet, RestorePhonePasswordViewSet, EmailLinkConfirmationViewSet

urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    re_path(r'activate_link/(?P<token>[0-9A-Za-z_\-]+)/(?P<confirmation_code>[0-9A-Za-z]{1,13})/$',
            EmailLinkConfirmationViewSet.activate, name='api_link'),
    ]

router = routers.DefaultRouter()
router.register(r'confirm_email', EmailConfirmationViewSet, basename='api_confirm_email')
router.register(r'confirm_link_email', EmailLinkConfirmationViewSet, basename='api_confirm_link_email')
router.register(r'confirm_phone', PhoneConfirmationViewSet, basename='api_confirm_phone')
router.register(r'restore_email_password', RestoreEmailPasswordViewSet, basename='api_restore_email_password')
router.register(r'restore_phone_password', RestorePhonePasswordViewSet, basename='api_restore_phone_password')
urlpatterns += router.urls
