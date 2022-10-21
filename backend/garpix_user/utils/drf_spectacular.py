from drf_spectacular.utils import OpenApiParameter
from django.utils.translation import gettext as _
from garpix_user.models import UserSession


def user_session_token_header_parameter(required=False):
    return OpenApiParameter(
        name=UserSession.HEAD_NAME,
        description=_('Unlogged user token'),
        required=required,
        type=str,
        location=OpenApiParameter.HEADER
    )
