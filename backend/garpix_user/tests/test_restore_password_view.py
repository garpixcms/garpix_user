import pytest
from django.core.exceptions import ValidationError
from garpix_user.views import RestorePasswordView
from garpix_user.serializers import RestorePasswordSerializer, RestoreCheckCodeSerializer, RestoreSetPasswordSerializer
from garpix_user.models import UserSession
from rest_framework.test import APIRequestFactory
from rest_framework.exceptions import MethodNotAllowed

USER_DATA = {
    'username': 'test_user',
    'password': 'test_password'
}
RESTORE_DATA = {
    'username': 'test_user',
    'restore_password_confirm_code': '123456'
}
SET_DATA = {
    'username': 'test_user',
    'restore_password_confirm_code': '123456',
    'new_password': 'new_password'
}

USER_SESSION = UserSession(id=1, user=USER_DATA)


class MockUserSession:
    def __init__(self, result, error):
        self.result = result
        self.error = error

    def send_restore_code(self, username):
        return self.result, self.error

    def check_restore_code(self, username, restore_password_confirm_code):
        return self.result, self.error

    def restore_password(self, new_password, username, restore_password_confirm_code):
        return self.result, self.error


@pytest.mark.django_db
class TestRestorePasswordView:

    def setup(self):
        self.view = RestorePasswordView()
        self.factory = APIRequestFactory()

    def test_send_code_success(self):  #Проверяет, что при выполнении действительного запроса на отправку кода восстановления, представление возвращает успешный ответ с ожидаемыми данными.
        user_session = MockUserSession(result=True, error=None)
        UserSession.get_from_request = lambda request: user_session

        request = self.factory.post('/', data=RESTORE_DATA)
        response = self.view.send_code(request)
        assert response.status_code == 200
        assert response.data == {'result': 'success'}

    def test_send_code_invalid_request(self):  #Проверяет, что при выполнении недействительного запроса (не POST-запрос) на отправку кода восстановления, представление raises MethodNotAllowed исключение.
        request = self.factory.post('/')
        with pytest.raises(MethodNotAllowed):
            self.view.send_code(request)

    def test_send_code_user_session_not_set(self):  #Проверяет, что когда сеанс пользователя не установлен, представление возвращает ответ с кодом 400 Bad Request с ожидаемым сообщением об ошибке.
        UserSession.get_from_request = lambda request: None
        request = self.factory.post('/', data=RESTORE_DATA)
        response = self.view.send_code(request)
        assert response.status_code == 400
        assert response.data == {'non_field_errors': ['user-session-token not set']}

    def test_send_code_error(self):  #Проверяет, что когда возникает ошибка во время операции отправки кода, представление raises ожидаемое ValidationError.
        user_session = MockUserSession(result=False, error=ValidationError('Error'))
        UserSession.get_from_request = lambda request: user_session

        request = self.factory.post('/', data=RESTORE_DATA)
        with pytest.raises(ValidationError) as e:
            self.view.send_code(request)
        assert str(e.value) == 'Error'

    def test_check_code_success(self):  #Проверяет, что при выполнении действительного запроса на проверку кода восстановления, представление возвращает успешный ответ с ожидаемыми данными.
        user_session = MockUserSession(result=True, error=None)
        UserSession.get_from_request = lambda request: user_session

        request = self.factory.post('/', data=RESTORE_DATA)
        response = self.view.check_code(request)
        assert response.status_code == 200
        assert response.data == {'result': 'success'}

    def test_check_code_user_session_not_set(self):  #Проверяет, что когда сеанс пользователя не установлен, представление возвращает ответ с кодом 400 Bad Request с ожидаемым сообщением об ошибке
        UserSession.get_from_request = lambda request: None

        request = self.factory.post('/', data=RESTORE_DATA)
        response = self.view.check_code(request)
        assert response.status_code == 400
        assert response.data == {'non_field_errors': ['user-session-token not set']}

    def test_check_code_error(self):  #Проверяет, что когда возникает ошибка во время операции проверки кода, представление raises ожидаемое ValidationError
        user_session = MockUserSession(result=False, error=ValidationError('Error'))
        UserSession.get_from_request = lambda request: user_session

        request = self.factory.post('/', data=RESTORE_DATA)
        with pytest.raises(ValidationError) as e:
            self.view.check_code(request)
        assert str(e.value) == 'Error'

    def test_set_password_success(self):  #Проверяет, что при выполнении действительного запроса на установку нового пароля, представление возвращает успешный ответ с ожидаемыми данными.
        user_session = MockUserSession(result=True, error=None)
        UserSession.get_from_request = lambda request: user_session

        request = self.factory.post('/', data=SET_DATA)
        response = self.view.set_password(request)
        assert response.status_code == 200
        assert response.data == {'result': 'success'}

    def test_set_password_user_session_not_set(self):  #Проверяет, что когда сеанс пользователя не установлен, представление возвращает ответ с кодом 400 Bad Request с ожидаемым сообщением об ошибке.
        UserSession.get_from_request = lambda request: None

        request = self.factory.post('/', data=SET_DATA)
        response = self.view.set_password(request)
        assert response.status_code == 400
        assert response.data == {'non_field_errors': ['user-session-token not set']}

    def test_set_password_error(self):
        user_session = MockUserSession(result=False, error=ValidationError('Error'))
        UserSession.get_from_request = lambda request: user_session

        request = self.factory.post('/', data=SET_DATA)
        with pytest.raises(ValidationError) as e:
            self.view.set_password(request)
        assert str(e.value) == 'Error'