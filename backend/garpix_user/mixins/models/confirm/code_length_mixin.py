from django.conf import settings


class CodeLengthMixin:

    def get_confirm_code_length(self, type='email'):
        GARPIX_USER_SETTINGS = getattr(settings, "GARPIX_USER", {})

        if type == 'email':

            MAX_LENGTH, CONFIRM_CODE_LENGTH = 255, GARPIX_USER_SETTINGS.get('CONFIRM_EMAIL_CODE_LENGTH', 6)
        else:
            MAX_LENGTH, CONFIRM_CODE_LENGTH = 15, GARPIX_USER_SETTINGS.get('CONFIRM_PHONE_CODE_LENGTH', 6)

        code_length = 4 if CONFIRM_CODE_LENGTH < 4 else MAX_LENGTH if CONFIRM_CODE_LENGTH > MAX_LENGTH else CONFIRM_CODE_LENGTH

        return code_length

    class Meta:
        abstract = True
