# Generated by Django 2.0.1 on 2018-11-14 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0004_auto_20181113_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracionbda',
            name='uitima_exportacion',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='configuracionbda',
            name='ultima_importacion',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='configuracionbda',
            name='ultimo_respaldo',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
