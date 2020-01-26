# Generated by Django 3.0.1 on 2020-01-07 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0005_auto_20200107_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='tipo_pessoa',
            field=models.CharField(choices=[('V', 'Visitante'), ('F', 'Frequentador'), ('M', 'Membro')], max_length=1),
        ),
    ]