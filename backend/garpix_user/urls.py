from django.urls import path
from garpix_user.views import obtain_auth_token, refresh_token_view, logout_view

urlpatterns = [
    path('login/', obtain_auth_token, name='api_login'),
    path('refresh/', refresh_token_view, name='api_refresh'),
    path('logout/', logout_view, name='api_logout')
]
