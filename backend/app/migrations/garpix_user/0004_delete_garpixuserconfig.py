# Generated by Django 3.2.15 on 2022-09-21 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('garpix_user', '0003_alter_usersession_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GarpixUserConfig',
        ),
    ]
