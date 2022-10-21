# Generated by Django 3.2.16 on 2022-10-21 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('garpix_user', '0004_delete_garpixuserconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='last_access',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last entrance'),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='recognized',
            field=models.PositiveIntegerField(choices=[(0, 'Undefined'), (1, 'Guest'), (2, 'Registered')], default=0, help_text='Indicates the state in which the user is recognized.', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='usersession',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]