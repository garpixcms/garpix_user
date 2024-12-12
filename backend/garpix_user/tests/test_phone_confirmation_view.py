import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from garpix_user.views import PhoneConfirmationView

User = get_user_model()


@pytest.mark.django_db
class TestPhoneConfirmationView:
    def setup_method(self):
        self.factory = RequestFactory()
        self.view = PhoneConfirmationView.as_view({'post': 'send_code', 'check_code': 'check_code'})

    def test_send_code_for_authenticated_user(self):  #Проверяет, что аутентифицированный пользователь может успешно отправить код подтверждения телефона.
        user = User.objects.create_user(username='testuser', password='testpassword')
        request = self.factory.post('/phone-confirmation/send-code/', {'phone': '+79001234567'}, format='json')
        request.user = user
        response = self.view(request, 'send_code')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'success'

    def test_send_code_for_unauthenticated_user_with_preregistration(self, settings):  #Проверяет, что неаутентифицированный пользователь может успешно отправить код подтверждения телефона, если настройка USE_PREREGISTRATION_PHONE_CONFIRMATION включена.
        settings.GARPIX_USER['USE_PREREGISTRATION_PHONE_CONFIRMATION'] = True
        request = self.factory.post('/phone-confirmation/send-code/', {'phone': '+79001234567'}, format='json')
        request.user = AnonymousUser()
        response = self.view(request, 'send_code')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'success'

    def test_send_code_for_unauthenticated_user_without_preregistration(self, settings):  #Проверяет, что неаутентифицированный пользователь не может отправить код подтверждения телефона, если настройка `USEPREREGISTRATIONPHONECONFIRMATION выключена.
        settings.GARPIX_USER['USE_PREREGISTRATION_PHONE_CONFIRMATION'] = False
        request = self.factory.post('/phone-confirmation/send-code/', {'phone': '+79001234567'}, format='json')
        request.user = AnonymousUser()
        with pytest.raises(NotAuthenticated):
            self.view(request, 'send_code')

    def test_check_code_for_authenticated_user(self):  #Проверяет, что аутентифицированный пользователь может успешно проверить код подтверждения телефона.
        user = User.objects.create_user(username='testuser', password='testpassword')
        request = self.factory.post('/phone-confirmation/check-code/', {'phone_confirmation_code': '123456'}, format='json')
        request.user = user
        response = self.view(request, 'check_code')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'success'

    def test_check_code_for_unauthenticated_user_with_preregistration(self, settings):  #Проверяет, что неаутентифицированный пользователь может успешно проверить код подтверждения телефона, если настройка USEPREREGISTRATIONPHONECONFIRMATION` включена.
        settings.GARPIX_USER['USE_PREREGISTRATION_PHONE_CONFIRMATION'] = True
        request = self.factory.post('/phone-confirmation/check-code/', {'phone_confirmation_code': '123456'}, format='json')
        request.user = AnonymousUser()
        response = self.view(request, 'check_code')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['result'] == 'success'

    def test_check_code_for_unauthenticated_user_without_preregistration(self, settings):  # Проверяет, что неаутентифицированный пользователь не может проверить код подтверждения телефона, если настройка USE_PREREGISTRATION_PHONE_CONFIRMATION выключена.
        settings.GARPIX_USER['USE_PREREGISTRATION_PHONE_CONFIRMATION'] = False
        request = self.factory.post('/phone-confirmation/check-code/', {'phone_confirmation_code': '123456'}, format='json')
        request.user = AnonymousUser()
        with pytest.raises(NotAuthenticated):
            self.view(request, 'check_code')
