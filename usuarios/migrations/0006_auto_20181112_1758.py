# Generated by Django 2.0.1 on 2018-11-12 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_auto_20181112_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntausuario',
            name='respuesta',
            field=models.CharField(max_length=80, verbose_name='Respuesta'),
        ),
    ]
