import pytest

from django.contrib.auth import get_user_model
from django.test import Client
from garpix_user.serializers import RegistrationSerializer


@pytest.mark.django_db
class TestRegistrationView:
    def setup_method(self):
        self.client = Client()

    def teardown_method(self): 
        get_user_model().objects.all().delete()

    def test_valid_registration(self):  #Проверяет, что при предоставлении корректных данных для регистрации, представление успешно создает нового пользователя.
        data = {"username": "test_user", "email": "test@example.com", "password": "strong_password"}
        response = self.client.post("/api/v1/registration/", data=data)

        assert response.status_code == 201
        assert get_user_model().objects.filter(username="test_user").exists()

    def test_invalid_username(self):  #Проверяет, что при предоставлении пустого имени пользователя, представление возвращает ответ с ошибкой.
        data = {"username": "", "email": "test@example.com", "password": "strong_password"}
        response = self.client.post("/api/v1/registration/", data=data)

        assert response.status_code == 400
        assert "This field may not be blank." in response.data["username"]

    def test_invalid_email(self):  #Проверяет, что при предоставлении некорректного адреса электронной почты, представление возвращает ответ с ошибкой.
        data = {"username": "test_user", "email": "invalid_email", "password": "strong_password"}
        response = self.client.post("/api/v1/registration/", data=data)

        assert response.status_code == 400
        assert "Enter a valid email address." in response.data["email"]

    def test_invalid_password(self):  #Проверяет, что при предоставлении пустого пароля, представление возвращает ответ с ошибкой.
        data = {"username": "test_user", "email": "test@example.com", "password": ""}
        response = self.client.post("/api/v1/registration/", data=data)

        assert response.status_code == 400
        assert "This field may not be blank." in response.data["password"]

    def test_serializer_validation(self):  #Проверяет, что сериализатор RegistrationSerializer работает правильно с пустыми данными.
        serializer = RegistrationSerializer(data={})
        assert not serializer.is_valid()
        assert serializer.errors == {
            "username": ["This field may not be blank."],
            "email": ["This field may not be blank.", "Enter a valid email address."],
            "password": ["This field may not be blank."],
        }
