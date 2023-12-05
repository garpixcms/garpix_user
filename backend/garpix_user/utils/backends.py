from django.contrib.auth import get_user_model
from django.db.models import Q
from garpix_utils.logs.enums.get_enums import Action, ActionResult
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.services.logger_iso import LoggerIso

from garpix_user.utils.get_password_settings import get_password_settings


class CustomAuthenticationBackend:
    def authenticate(self, request, username=None, password=None):
        password_settings = get_password_settings()

        if username is None or password is None:
            return None
        try:
            query = Q()
            for field in get_user_model().USERNAME_FIELDS:
                query |= Q(**{field: username.lower()})
            user = get_user_model().active_objects.get(query)
            pwd_valid = user.check_password(password)
            if pwd_valid:
                user.login_attempts_count = 0
                user.save()
                return user
            user.login_attempts_count += 1
            if password_settings['available_attempt'] != -1 and user.login_attempts_count >= password_settings[
                    'available_attempt']:
                user.is_blocked = True

                message = f'Пользователь {user.username} заблокирован'

                log = ib_logger.create_log(action=Action.user_access.value,
                                           obj=get_user_model().__name__,
                                           obj_address=request.path,
                                           result=ActionResult.success,
                                           sbj=user.username,
                                           sbj_address=LoggerIso.get_client_ip(request),
                                           msg=message)

                ib_logger.write_string(log)

            user.save()
            return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().active_objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
