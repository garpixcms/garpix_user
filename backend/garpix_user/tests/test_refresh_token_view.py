import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from garpix_user.models import RefreshToken
from garpix_user.serializers import RefreshTokenSerializer
from garpix_user.views import RefreshTokenView

User = get_user_model()


@pytest.mark.django_db
class TestRefreshTokenView:
    def setup_method(self):
        self.user = User.objects.create_user(username='test_user', password='test_pass')
        self.refresh_token = RefreshToken.objects.create(user=self.user, key='test_refresh_token')
        self.view = RefreshTokenView.as_view()

    def test_valid_refresh_token(self, rf):  #Проверяет, что при предоставлении действительного refresh-токена, представление возвращает ответ с обновленным access-токеном и временем его истечения.
        data = {'refresh_token': 'test_refresh_token'}
        request = rf.post('/api/v1/refresh-token/', data=data)
        response = self.view(request)
        assert response.status_code == 200
        assert 'access_token' in response.data
        assert 'access_token_expires' in response.data
        assert response.data['result'] is True

    def test_expired_refresh_token(self, rf):  #Проверяет, что при использовании просроченного refresh-токена, представление возвращает ответ с ошибкой.
        self.refresh_token.created = timezone.now() - timezone.timedelta(seconds=61)
        self.refresh_token.save()
        data = {'refresh_token': 'test_refresh_token'}
        request = rf.post('/api/v1/refresh-token/', data=data)
        response = self.view(request)
        assert response.status_code == 400
        assert 'result' in response.data
        assert response.data['result'] is False

    def test_invalid_refresh_token(self, rf):  #Проверяет, что при использовании недействительного refresh-токена, представление возвращает ответ с ошибкой.
        data = {'refresh_token': 'invalid_refresh_token'}
        request = rf.post('/api/v1/refresh-token/', data=data)
        response = self.view(request)
        assert response.status_code == 400
        assert 'result' in response.data
        assert response.data['result'] is False

    def test_invalid_json(self, rf):  #Проверяет, что при отправке некорректных данных в формате JSON, представление возвращает ответ с ошибкой.
        data = {'invalid_json': 'test'}
        request = rf.post('/api/v1/refresh-token/', data=data)
        response = self.view(request)
        assert response.status_code == 400

    def test_valid_serializer(self):  #Проверяет, что сериализатор RefreshTokenSerializer работает правильно с действительными данными.
        serializer = RefreshTokenSerializer(data={'refresh_token': 'test_refresh_token'})
        assert serializer.is_valid()

    def test_invalid_serializer(self):  #Проверяет, что сериализатор RefreshTokenSerializer работает правильно с недействительными данными.
        serializer = RefreshTokenSerializer(data={'invalid_field': 'test'})
        assert not serializer.is_valid()
