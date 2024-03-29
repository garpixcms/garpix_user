# Generated by Django 3.2.23 on 2024-01-18 09:09

from django.db import migrations, models
import garpix_user.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_user', '0018_garpixuserpasswordconfiguration_access_tokens_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='garpixuserpasswordconfiguration',
            name='access_tokens_count',
            field=models.IntegerField(default=-1, help_text='-1 если отправка уведомлений не требуется', validators=[garpix_user.utils.validators.PositiveWithInfValidator], verbose_name='Количество хранимых access-токенов (самый старый будет удален)'),
        ),
    ]
