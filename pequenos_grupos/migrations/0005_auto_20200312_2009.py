# Generated by Django 3.0.1 on 2020-03-12 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0012_auto_20200304_2251'),
        ('pequenos_grupos', '0004_celula_participantes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='celula',
            name='situacao',
        ),
        migrations.AddField(
            model_name='celula',
            name='ativo',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='celula',
            name='participantes',
            field=models.ManyToManyField(to='pessoas.Pessoa'),
        ),
    ]
