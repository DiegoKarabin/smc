# Generated by Django 2.0.1 on 2018-11-13 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0011_auto_20181113_0745'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_editing',
            field=models.CharField(default=0, max_length=9),
        ),
    ]
