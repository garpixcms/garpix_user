from django.utils.translation import activate


class ActivateTranslationMixin:
    def initialize_request(self, request, *args, **kwargs):
        init_request = super().initialize_request(request, *args, **kwargs)
        activate(request.headers.get('Accept-Language', 'en'))
        return init_request
