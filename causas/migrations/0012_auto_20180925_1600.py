# Generated by Django 2.0.1 on 2018-09-25 20:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('causas', '0011_auto_20180607_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='triaje',
            name='proxima_cita',
            field=models.DateField(default=datetime.date(2018, 10, 2)),
        ),
    ]
