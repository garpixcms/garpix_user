import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from garpix_user.exceptions import NotAuthenticateException
from backend.garpix_user.models import PasswordHistory
from backend.garpix_user.utils.get_password_settings import get_password_settings

User = get_user_model()


@pytest.mark.django_db
class TestChangePasswordView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='oldpassword')
        self.change_password_url = reverse('change-password')
        self.change_password_unauthorized_url = reverse('change-password-unauthorized')

    def test_change_password_for_authenticated_user(self):  #Проверяет, что аутентифицированный пользователь может успешно изменить свой пароль.
        self.client.force_authenticate(user=self.user)
        data = {'old_password': 'oldpassword', 'new_password': 'newpassword'}
        response = self.client.post(self.change_password_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'result': 'success'}
        self.user.refresh_from_db()
        assert self.user.check_password('newpassword')

    def test_change_password_for_unauthenticated_user(self):  #Проверяет, что неаутентифицированный пользователь не может изменить пароль и получает ошибку 403 Forbidden.
        data = {'old_password': 'oldpassword', 'new_password': 'newpassword'}
        response = self.client.post(self.change_password_url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert isinstance(response.exception, NotAuthenticateException)

    def test_change_password_for_keycloak_auth_only_user(self):  #Проверяет, что пользователь, аутентифицированный только через Keycloak, не может изменить свой пароль и получает соответствующее сообщение об ошибке.
        self.user.keycloak_auth_only = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        data = {'old_password': 'oldpassword', 'new_password': 'newpassword'}
        response = self.client.post(self.change_password_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'new_password': ['You can not change your password. Please contact administrator']}

    def test_change_password_for_unauthorized_user(self):  #Проверяет, что пользователь без аутентификации может изменить пароль другого пользователя через специальный URL-адрес
        data = {'username': 'testuser', 'new_password': 'newpassword'}
        response = self.client.post(self.change_password_unauthorized_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        self.user.refresh_from_db()
        assert self.user.check_password('newpassword')
        assert not self.user.needs_password_update

    def test_password_history_check(self, monkeypatch):  #Проверяет, что пользователь не может использовать пароль, который уже был использован в прошлом
        monkeypatch.setattr(get_password_settings(), 'password_history', 2)
        self.client.force_authenticate(user=self.user)
        PasswordHistory.objects.create(user=self.user, password='oldpassword')
        PasswordHistory.objects.create(user=self.user, password='newpassword')
        data = {'old_password': 'oldpassword', 'new_password': 'oldpassword'}
        response = self.client.post(self.change_password_url, data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {'new_password': ['You can not use the same password you already had to']}
