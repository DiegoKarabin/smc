# Generated by Django 2.0.1 on 2018-11-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0002_auto_20180513_2248'),
    ]

    operations = [
        migrations.AddField(
            model_name='persona',
            name='edit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='persona',
            name='is_editing',
            field=models.CharField(default=0, max_length=9),
        ),
    ]