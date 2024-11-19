import pytest
from django.urls import reverse
from django.test import RequestFactory
from garpix_user.models import ReferralType
from garpix_user.views.referral_links_view import ReferralLinkView
from backend.app import settings


@pytest.mark.django_db
def test_referral_link_view_success(mocker):  #Проверяет, что при успешном использовании реферальной ссылки, пользователь будет перенаправлен на URL, определенный в настройке REFERRAL_REDIRECT_URL.
    factory = RequestFactory()
    request = factory.get(reverse('referral_link', kwargs={'hash': 'testhash'}))
    view = ReferralLinkView.as_view()
    mocker.patch('garpix_user.models.ReferralType.objects.get', return_value=ReferralType(referral_hash='testhash'))
    mocker.patch('garpix_user.models.ReferralUserLink.objects.create', return_value=None)
    mocker.patch('garpix_user.models.UserSession.get_or_create_user_session', return_value='testuser')
    response = view(request, hash='testhash')
    assert response.url == f"{settings.GARPIX_USER.get('REFERRAL_REDIRECT_URL', '/')}?status=success"


@pytest.mark.django_db
def test_referral_link_view_error(mocker):  #Проверяет, что при ошибке обработки реферальной ссылки, пользователь будет перенаправлен на URL, определенный в настройке REFERRAL_REDIRECT_URL.
    factory = RequestFactory()
    request = factory.get(reverse('referral_link', kwargs={'hash': 'testhash'}))
    view = ReferralLinkView.as_view()
    mocker.patch('garpix_user.models.ReferralType.objects.get', side_effect=Exception('Not found'))
    mocker.patch('garpix_user.models.UserSession.get_or_create_user_session', return_value='testuser')
    response = view(request, hash='testhash')

    assert response.url == f"{settings.GARPIX_USER.get('REFERRAL_REDIRECT_URL', '/')}?status=error"
