# Generated by Django 2.0.1 on 2018-11-08 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_auto_20181106_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_password_setted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usuario',
            name='is_security_question_setted',
            field=models.BooleanField(default=False),
        ),
    ]