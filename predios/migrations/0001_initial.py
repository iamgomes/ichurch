# Generated by Django 3.0.1 on 2019-12-28 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Predio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnpj', models.CharField(blank=True, max_length=18, null=True)),
                ('nome', models.CharField(max_length=100)),
                ('data_abertura', models.DateField(blank=True, null=True, verbose_name='Data Abertura')),
                ('telefone', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, verbose_name='E-mail')),
                ('cep', models.CharField(blank=True, max_length=9, null=True)),
                ('rua', models.CharField(blank=True, max_length=200, null=True)),
                ('numero', models.IntegerField(blank=True, null=True)),
                ('bairro', models.CharField(blank=True, max_length=50, null=True)),
                ('cidade', models.CharField(blank=True, max_length=50, null=True)),
                ('uf', models.CharField(blank=True, max_length=50, null=True)),
                ('pais', models.CharField(blank=True, max_length=50, null=True)),
                ('tipo_igreja', models.CharField(choices=[('P', 'PIB Imperial'), ('A', 'Associada')], default='P', max_length=1)),
                ('created', models.DateField(auto_now_add=True, verbose_name='Data Cadastro')),
                ('updated', models.DateField(auto_now=True, verbose_name='Data Atualização')),
            ],
        ),
    ]