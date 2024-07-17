import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from app.settings import GARPIX_USER


User = get_user_model()


@pytest.mark.django_db
class TestObtainAuthToken:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.url = reverse('obtain-auth-token')

    def test_obtain_auth_token_with_valid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data

    def test_obtain_auth_token_with_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data

    def test_obtain_auth_token_with_jwt(self, mocker):
        GARPIX_USER['REST_AUTH_TOKEN_JWT'] = True
        mock_jwt_data = mocker.patch('garpix_user.views.ObtainAuthToken._get_jwt_data', return_value={'access_token': 'test_access_token'})
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access_token' in response.data
        mock_jwt_data.assert_called_with(self.user)

    def test_obtain_auth_token_without_jwt(self, mocker):
        GARPIX_USER['REST_AUTH_TOKEN_JWT'] = False
        mock_access_token_data = mocker.patch('garpix_user.views.ObtainAuthToken._get_access_token_data', return_value={'token': 'test_token'})

        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'token' in response.data
        mock_access_token_data.assert_called_with(self.user)

    def test_obtain_auth_token_logs_user_login(self, mocker):
        mock_create_log = mocker.patch('garpix_user.logger.IbLogger.create_log')
        mock_write_string = mocker.patch('garpix_user.logger.IbLogger.write_string')

        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        assert response.status_code == status.HTTP_200_OK
        mock_create_log.assert_called()
        mock_write_string.assert_called()
