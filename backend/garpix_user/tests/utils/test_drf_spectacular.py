from rest_framework.test import APITestCase
from drf_spectacular.utils import OpenApiParameter
from django.utils.translation import gettext as _
from garpix_user.models import UserSession

from garpix_user.utils.drf_spectacular import user_session_token_header_parameter

class UserSessionTokenHeaderParameter(APITestCase):
    def test_user_session_token_header_parameter(self) -> None:
        parameter = user_session_token_header_parameter(required=True)
        self._check_open_api_params(parameter)
        self.assertEqual(parameter.required, True)

        parameter = user_session_token_header_parameter(required=False)
        self._check_open_api_params(parameter)
        self.assertEqual(parameter.required, False)
    
    def _check_open_api_params(self, parameter: OpenApiParameter) -> None:
        self.assertEqual(parameter.name, UserSession.HEAD_NAME)
        self.assertEqual(parameter.description, _('Unlogged user token'))
        self.assertEqual(parameter.type, str)
        self.assertEqual(parameter.location, OpenApiParameter.HEADER)
