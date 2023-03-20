from django.contrib.auth import get_user_model
from django.db.models import Q


class CustomAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        if username is None or password is None:
            return None
        try:
            query = Q()
            for field in get_user_model().USERNAME_FIELDS:
                query |= Q(**{field: username.lower()})
            user = get_user_model().active_objects.get(query)
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().active_objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
