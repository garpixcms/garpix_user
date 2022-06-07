"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from garpix_user.views.referral_links_view import ReferralLinkView
from .views import HomeView, CurrentUserView
from garpix_user.views.login_views import LogoutView, LoginView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings

urlpatterns = [
    path('', HomeView.as_view()),
    path('admin/', admin.site.urls),
    path('api/current-user/', CurrentUserView.as_view(), name='current-user'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # garpix_user
    path('logout/', LogoutView.as_view(url='/'), name="logout"),
    path('login/', LoginView.as_view(template_name="accounts/login.html"), name="authorize"),
    path('api/user/', include(('user.urls', 'user'), namespace='user')),
    re_path(r'hash/^(?P<hash>.*?)/$', ReferralLinkView.as_view(), name='referral_link'),
    re_path(r'hash/^(?P<hash>.*?)$', ReferralLinkView.as_view(), name='referral_link')
]


if settings.DEBUG:
    urlpatterns += [
        path(f'{settings.API_URL}/schema/', SpectacularAPIView.as_view(), name='schema'),
        path(f'{settings.API_URL}/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
