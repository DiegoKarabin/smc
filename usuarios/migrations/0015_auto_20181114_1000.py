# Generated by Django 2.0.1 on 2018-11-14 14:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_auto_20181114_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitacoraacceso',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='bitacoraacceso',
            name='registro',
            field=models.CharField(max_length=80),
        ),
    ]
