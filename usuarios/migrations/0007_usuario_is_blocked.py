# Generated by Django 2.0.1 on 2018-11-13 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auto_20181112_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
    ]
