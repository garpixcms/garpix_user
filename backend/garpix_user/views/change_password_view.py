from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import ugettext as _

from garpix_user.serializers import ChangePasswordSerializer
from garpix_user.utils.drf_spectacular import user_session_token_header_parameter


@extend_schema(
    parameters=[
        user_session_token_header_parameter()
    ]
)
class ChangePasswordView(viewsets.ViewSet):

    def get_serializer_class(self):
        return ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(summary=_('Change password (for authorized users)'))
    @action(methods=['POST'], detail=False)
    def change_password(self, request, *args, **kwargs):

        user = request.user

        serializer = self.get_serializer_class()(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user.set_password(request.data['new_password'])
        user.save()

        return Response({"result": "success"})
