# Generated by Django 2.0.1 on 2018-11-13 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0007_usuario_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='is_blocked',
            field=models.IntegerField(default=0),
        ),
    ]
