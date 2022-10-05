from django.db import models


class UserSessionMixin(models.Model):

    class Meta:
        abstract = True
