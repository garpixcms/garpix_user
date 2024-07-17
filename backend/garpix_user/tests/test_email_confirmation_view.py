import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from garpix_user.exceptions import NotAuthenticateException
from garpix_user.models import UserSession

User = get_user_model()


@pytest.mark.django_db
class TestEmailConfirmationView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com')
        self.send_code_url = reverse('email-confirmation-send-code')
        self.check_code_url = reverse('email-confirmation-check-code')

    def test_send_code_for_authenticated_user(self):  #Проверяет, что аутентифицированный пользователь может успешно отправить код подтверждения электронной почты.
        self.client.force_authenticate(user=self.user)
        data = {'email': 'testuser@example.com'}
        response = self.client.post(self.send_code_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'result': 'success'}

    def test_send_code_for_unauthenticated_user(self):  #Проверяет, что неаутентифицированный пользователь также может успешно отправить код подтверждения электронной почты.
        data = {'email': 'testuser@example.com'}
        response = self.client.post(self.send_code_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'result': 'success'}

    def test_check_code_for_authenticated_user(self):  #Проверяет, что аутентифицированный пользователь может успешно проверить код подтверждения электронной почты.
        self.client.force_authenticate(user=self.user)
        data = {'email_confirmation_code': '123456'}
        response = self.client.post(self.check_code_url, data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'result': 'success'}

    def test_check_code_for_unauthenticated_user(self):  #Проверяет, что неаутентифицированный пользователь не может проверить код подтверждения электронной почты и получает ошибку 403 Forbidden.
        data = {'email_confirmation_code': '123456'}
        response = self.client.post(self.check_code_url, data, format='json')
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert isinstance(response.exception, NotAuthenticateException)


@pytest.mark.django_db
class TestEmailConfirmationLinkView:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com')
        self.user_session = UserSession.objects.create(email='testuser@example.com')
        self.confirm_link_url = reverse('email-confirmation-link', kwargs={'hash': 'valid_hash', 'model_type': 'user'})
        self.confirm_link_user_session_url = reverse('email-confirmation-link', kwargs={'hash': 'valid_hash', 'model_type': 'user_session'})

    def test_confirm_email_by_link_for_user(self, mocker):  #Проверяет, что пользователь может успешно подтвердить свой адрес электронной почты, перейдя по ссылке подтверждения.
        mock_confirm = mocker.patch('garpix_user.models.User.confirm_email_by_link', return_value=(True, self.user))
        response = self.client.get(self.confirm_link_url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == '/?status=success'
        mock_confirm.assert_called_with('valid_hash')

    def test_confirm_email_by_link_for_user_session(self, mocker):  #Проверяет, что пользователь сеанса может успешно подтвердить свой адрес электронной почты, перейдя по ссылке подтверждения.
        mock_confirm = mocker.patch('garpix_user.models.UserSession.confirm_email_by_link', return_value=(True, self.user_session))
        response = self.client.get(self.confirm_link_user_session_url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == '/?status=success'
        mock_confirm.assert_called_with('valid_hash')

    def test_confirm_email_by_link_with_error(self, mocker):  #Проверяет, что если метод confirm_email_by_link возвращает False, пользователь перенаправляется на страницу с ошибкой.
        mock_confirm = mocker.patch('garpix_user.models.User.confirm_email_by_link', return_value=(False, None))
        response = self.client.get(self.confirm_link_url)
        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == '/?status=error'
        mock_confirm.assert_called_with('valid_hash')
