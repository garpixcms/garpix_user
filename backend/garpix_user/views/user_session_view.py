from typing import Optional

from drf_spectacular.utils import extend_schema
from rest_framework import parsers
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_user.models import UserSession
from ..serializers import UserSessionTokenSerializer
from ..utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class UserSessionView(viewsets.ViewSet):
    parser_classes = (parsers.JSONParser,)
    permission_classes = (permissions.AllowAny,)

    def get_user_session(self) -> Optional[UserSession]:
        return UserSession.get_from_request(self.request)

    def get_or_create_user_session(self, session=False):
        return UserSession.get_or_create_user_session(request=self.request, session=session)

    @action(detail=False, methods=['POST'], permission_classes=(permissions.AllowAny,))
    def create_user_session(self, request):
        return Response({
            'session_user': UserSessionTokenSerializer(self.get_or_create_user_session()).data
        }, status=status.HTTP_200_OK)
