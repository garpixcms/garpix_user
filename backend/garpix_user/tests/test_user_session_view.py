import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from garpix_user.models import UserSession
from garpix_user.views.user_session_view import UserSessionView


@pytest.mark.django_db
def test_create_user_session_success(mocker):
    factory = APIRequestFactory()
    request = factory.post(reverse('usersession-create-user-session'), {}, format='json')
    view = UserSessionView.as_view({'post': 'create_user_session'})
    mocker.patch('garpix_user.models.UserSession.get_or_create_user_session', return_value=UserSession(id=1, user='testuser'))
    mocker.patch('garpix_user.serializers.UserSessionTokenSerializer.data', return_value={'id': 1, 'user': 'testuser'})
    response = view(request)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['session_user'] == {'id': 1, 'user': 'testuser'}


@pytest.mark.django_db
def test_create_user_session_failure(mocker):
    factory = APIRequestFactory()
    request = factory.post(reverse('usersession-create-user-session'), {}, format='json')
    view = UserSessionView.as_view({'post': 'create_user_session'})
    mocker.patch('garpix_user.models.UserSession.get_or_create_user_session', side_effect=Exception('Error'))
    response = view(request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
