from rest_framework.test import APITestCase
from rest_framework.request import HttpRequest

from garpix_user.utils.get_token_from_request import get_token_from_request


class GetTokenFromRequest(APITestCase):
    def test_get_token_from_request(self) -> None:
        request = HttpRequest()
        request.META["HTTP_AUTHORIZATION"] = "Bearer test_token"
        self.assertEqual(get_token_from_request(request), "test_token")
    
    def test_get_token_from_request_none(self) -> None:
        self.assertIsNone(get_token_from_request(HttpRequest()))
