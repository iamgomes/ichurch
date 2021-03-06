# Generated by Django 3.0.1 on 2020-01-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pequenos_grupos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='celula',
            name='bairro',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='cep',
            field=models.CharField(blank=True, max_length=9, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='cidade',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='complemento',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='numero',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='pais',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='rua',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='celula',
            name='uf',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
