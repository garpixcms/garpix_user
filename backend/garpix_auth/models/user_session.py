import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.module_loading import import_string


UserSessionMixin = import_string(settings.GARPIX_USER_USERSESSION_MIXIN)


class UserSession(UserSessionMixin, models.Model):
    HEAD_NAME = 'UserSession-Token'

    class UserState(models.IntegerChoices):
        UNRECOGNIZED = (0, 'Неопознанный')
        GUEST = (1, 'Гость')
        REGISTERED = (2, 'Зарегистрированный')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    number = models.CharField(max_length=256, null=True, blank=True, verbose_name='user token')
    recognized = models.PositiveIntegerField(
        default=UserState.UNRECOGNIZED,
        choices=UserState.choices,
        verbose_name='Тип',
        help_text='Обозначает состояние, в котором распознается пользователь.'
    )
    last_access = models.DateTimeField(
        'Последний вход',
        default=timezone.now,
    )

    @classmethod
    def get_from_request(cls, request):
        user = request.user
        if user.is_authenticated:
            return UserSession.objects.filter(user=user).first()

        token = request.headers.get(cls.HEAD_NAME, None)
        if token is not None:
            return UserSession.objects.filter(number=token).first()

        token = request.session.session_key
        if token is not None:
            return UserSession.objects.filter(number=token).first()
        return None

    @classmethod
    def set_user_from_request(cls, request):
        user_session = cls.get_from_request(request)
        if request.user.is_authenticated and user_session is not None:
            user = get_user_model().objects.get(pk=request.user.pk)
            user_session.user = user
            user_session.save()
            return True
        return False

    @classmethod
    def get_or_create_sessionuser(cls, request, session=False):
        user_session = cls.get_from_request(request)
        if user_session is not None:
            return user_session

        if request.user.is_authenticated:
            user = get_user_model().objects.get(pk=request.user.pk)
            return UserSession.objects.create(
                user=user,
                recognized=UserSession.UserState.REGISTERED
            )

        if session is True:
            token = request.session.session_key
            return UserSession.objects.create(
                number=token,
                recognized=UserSession.UserState.GUEST
            )

        return UserSession.objects.create(
            number=uuid.uuid4(),
            recognized=UserSession.UserState.GUEST
        )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.pk}'