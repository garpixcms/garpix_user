from garpix_user.mixins.models import GarpixUserMixin


class User(GarpixUserMixin):

    USERNAME_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
