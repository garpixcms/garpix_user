# Generated by Django 3.2.16 on 2022-11-03 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_notify', '0004_auto_20221026_0656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='event',
            field=models.IntegerField(blank=True, choices=[(4210, 'Подтверждение номера телефона'), (4211, 'Подтверждение email'), (4212, 'Восстановление пароля по email'), (4213, 'Восстановление пароля по номеру телефона'), (4214, 'Подтверждение email по ссылке')], null=True, verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='notifytemplate',
            name='event',
            field=models.IntegerField(blank=True, choices=[(4210, 'Подтверждение номера телефона'), (4211, 'Подтверждение email'), (4212, 'Восстановление пароля по email'), (4213, 'Восстановление пароля по номеру телефона'), (4214, 'Подтверждение email по ссылке')], null=True, verbose_name='Событие'),
        ),
        migrations.AlterField(
            model_name='systemnotify',
            name='event',
            field=models.IntegerField(blank=True, choices=[(4210, 'Подтверждение номера телефона'), (4211, 'Подтверждение email'), (4212, 'Восстановление пароля по email'), (4213, 'Восстановление пароля по номеру телефона'), (4214, 'Подтверждение email по ссылке')], null=True, verbose_name='Событие'),
        ),
    ]