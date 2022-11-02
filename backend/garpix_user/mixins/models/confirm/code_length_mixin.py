from django.conf import settings


class CodeLengthMixin:

    def get_confirm_code_length(self):
        GARPIX_USER_SETTINGS = getattr(settings, "GARPIX_USER", {})
        code_length = 4 if (code_length := GARPIX_USER_SETTINGS.get('CONFIRM_CODE_LENGTH',
                                                                    6)) < 4 else (
            255 if code_length > 255 else code_length)

        return code_length

    class Meta:
        abstract = True
