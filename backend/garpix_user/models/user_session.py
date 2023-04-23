import uuid
from django.db import models
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from phonenumber_field.modelfields import PhoneNumberField

from garpix_user.mixins.models import RestorePasswordMixin
from garpix_user.mixins.models.confirm import UserEmailConfirmMixin, UserPhoneConfirmMixin


class UserSession(RestorePasswordMixin, UserEmailConfirmMixin, UserPhoneConfirmMixin, models.Model):
    HEAD_NAME = 'user-session-token'

    class UserState(models.IntegerChoices):
        UNRECOGNIZED = (0, _('Undefined'))
        GUEST = (1, _('Guest'))
        REGISTERED = (2, _('Registered'))

    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    is_email_confirmed = models.BooleanField(_("Email confirmed"), default=False)

    phone = PhoneNumberField(_("Phone number"), blank=True, default='')
    is_phone_confirmed = models.BooleanField(_("Phone number confirmed"), default=False)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('User')
    )
    token_number = models.CharField(max_length=256, null=True, blank=True, verbose_name='user token')
    recognized = models.PositiveIntegerField(
        default=UserState.UNRECOGNIZED,
        choices=UserState.choices,
        verbose_name=_('Type'),
        help_text=_('Indicates the state in which the user is recognized.')
    )
    last_access = models.DateTimeField(
        verbose_name=_('Last entrance'),
        default=timezone.now,
    )

    @classmethod
    def get_from_request(cls, request):
        user = request.user
        if user.is_authenticated:
            return UserSession.objects.filter(user=user).first()

        token = request.headers.get(cls.HEAD_NAME, None)

        if token is not None:
            user_session, _res = UserSession.objects.get_or_create(token_number=token)
            return user_session

        token = request.session.session_key
        if token is not None:
            return UserSession.objects.filter(token_number=token).first()

        username = request.GET.get('username', None)
        if username is not None:
            query = Q()
            for field in get_user_model().USERNAME_FIELDS:
                query |= Q(**{f'user__{field}': username.lower()})
            return UserSession.objects.filter(query).first()
        return None

    @classmethod
    def create_from_request(cls, request, username, session):

        User = get_user_model()

        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.pk)
            return UserSession.objects.create(
                user=user,
                token_number=uuid.uuid4(),
                recognized=UserSession.UserState.REGISTERED
            )

        if session is True:
            if not request.session.session_key:
                request.session.cycle_key()
            token = request.session.session_key
            return UserSession.objects.create(
                token_number=token,
                recognized=UserSession.UserState.GUEST
            )

        if username is not None:
            query = Q()
            for field in User.USERNAME_FIELDS:
                query |= Q(**{field: username.lower()})

            try:
                user = User.objects.get(query)
                session_user = UserSession.objects.filter(user=user).first()
                return session_user or UserSession.objects.create(
                    token_number=uuid.uuid4(),
                    recognized=UserSession.UserState.REGISTERED,
                    user=user
                )
            except Exception as e:
                print(e)

        return UserSession.objects.create(
            token_number=uuid.uuid4(),
            recognized=UserSession.UserState.GUEST
        )

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
    def get_or_create_user_session(cls, request, username=None, session=False):

        user_session = cls.get_from_request(request)
        if user_session is not None:
            return user_session

        return cls.create_from_request(request, username, session)

    class Meta:
        verbose_name = _('System user')
        verbose_name_plural = _('System users')

    def __str__(self):
        return _(
            f"{self.UserState.choices[self.recognized][1]} {self.user.username}" if self.user else f'{self.UserState.choices[self.recognized][1]} № {self.pk}')
