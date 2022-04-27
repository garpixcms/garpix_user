from django.urls import path
from rest_framework import routers

from garpix_auth.views import RegistrationView, obtain_auth_token, refresh_token_view, logout_view

from garpix_auth.viewsets import EmailConfirmationViewSet, PhoneConfirmationViewSet, RestorePasswordViewSet

urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout'),
    path('registration/', RegistrationView.as_view(), name='registration')
]

router = routers.DefaultRouter()
router.register(r'confirm_email', EmailConfirmationViewSet, basename='api_confirm_email')
router.register(r'confirm_phone', PhoneConfirmationViewSet, basename='api_confirm_phone')
router.register(r'restore_password', RestorePasswordViewSet, basename='api_restore_password')
urlpatterns += router.urls
