# Generated by Django 3.0.1 on 2020-03-05 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0011_auto_20200302_0205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='situacao',
        ),
        migrations.AddField(
            model_name='pessoa',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
    ]
