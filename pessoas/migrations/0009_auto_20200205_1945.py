# Generated by Django 3.0.1 on 2020-02-05 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0008_auto_20200203_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='lat',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='pessoa',
            name='lng',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
