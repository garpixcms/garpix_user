from typing import Optional

from drf_spectacular.utils import OpenApiParameter
from rest_framework import parsers
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from garpix_user.models import UserSession
from ..serializers import UserSessionSerializer


class UserSessionView(viewsets.ViewSet):
    parser_classes = (parsers.JSONParser,)
    permission_classes = (permissions.AllowAny,)

    header_parameter = OpenApiParameter(
        name=UserSession.HEAD_NAME,
        description='UserSession',
        required=True,
        type=str,
        location=OpenApiParameter.HEADER
    )

    def get_user_session(self) -> Optional[UserSession]:
        return UserSession.get_from_request(self.request)

    def get_or_create_user_session(self, session=False):
        return UserSession.get_or_create_user_session(request=self.request, session=session)

    @action(detail=False, methods=['POST'], permission_classes=(permissions.AllowAny,))
    def create_user_session(self, request):
        return Response({
            'session_user': UserSessionSerializer(self.get_or_create_user_session()).data
        }, status=status.HTTP_200_OK)
