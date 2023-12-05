import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.views.generic.base import RedirectView
from django.views.generic import FormView
from django.http import HttpResponse
from garpix_utils.logs.enums.get_enums import Action, ActionResult
from garpix_utils.logs.loggers import ib_logger
from garpix_utils.logs.services.logger_iso import LoggerIso

from garpix_user.forms import LoginForm
from django.utils.translation import ugettext as _


class LogoutView(RedirectView):

    def get_redirect_url(self):

        request = self.request
        logout(request)

        message = f'Пользователь {request.user.username} вышел из системы.'
        log = ib_logger.create_log(action=Action.user_logout.value,
                                   obj=get_user_model().__name__,
                                   obj_address=request.path,
                                   result=ActionResult.success,
                                   sbj=request.user.username,
                                   sbj_address=LoggerIso.get_client_ip(request),
                                   msg=message)

        ib_logger.write_string(log)

        return self.url


class LoginView(UserPassesTestMixin, FormView):
    http_method_names = ['post']

    def http_method_not_allowed(self, request, *args, **kwargs):
        if self.request.accepts('text/html'):
            return redirect(self.request.GET.get('next', '/') or '/')
        return HttpResponseNotAllowed(self._allowed_methods())

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        if self.request.accepts('text/html'):
            return redirect(self.request.GET.get('next', '/') or '/')
        return HttpResponse({"__all__": [_("You are already authenticated")]}, content_type='application/json',
                            status=403)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if not kwargs.get('data'):
            kwargs['data'] = json.loads(getattr(self.request, 'body') or b'{}')
        return kwargs

    @staticmethod
    def get_form_class(**kwargs):
        return LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def _return_error(self, form, error_text):
        try:
            form.add_error(None, error_text)
        except TypeError:
            pass
        return self.form_invalid(form)

    def form_valid(self, form):

        request = self.request
        data = form.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username.lower(), password=password)

        if user:
            user.set_user_session(request)
        login(request, user)

        if self.request.accepts('text/html'):
            return redirect(request.GET.get('next', '/') or '/')
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        if self.request.accepts('text/html'):
            return self.render_to_response(self.get_context_data(form=form))
        return HttpResponse(json.dumps(form.errors), content_type='application/json', status=400)
