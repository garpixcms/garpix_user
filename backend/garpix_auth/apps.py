from django.apps import AppConfig


class GarpixAuthConfig(AppConfig):
    name = 'garpix_auth'

    def ready(self):
        import garpix_auth.signals
