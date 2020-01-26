# Generated by Django 3.0.1 on 2020-01-24 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pessoas', '0007_auto_20200115_0057'),
        ('predios', '0005_predio_situacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Celula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo_celula', models.CharField(choices=[('A', 'Adultos'), ('J', 'Jovens'), ('C', 'Crianças'), ('M', 'Mista')], max_length=1)),
                ('dia_semana_reuniao', models.CharField(choices=[('1', 'Domingo'), ('2', 'Segunda-Feira'), ('3', 'Terça-Feira'), ('4', 'Quarta-Feira'), ('5', 'Quinta-Feira'), ('6', 'Sexta-Feira'), ('7', 'Sábado')], max_length=1)),
                ('hora_reuniao', models.TimeField(max_length=6)),
                ('situacao', models.CharField(choices=[('A', 'Ativo'), ('I', 'Inativo')], default='A', max_length=1)),
                ('created', models.DateField(auto_now_add=True, verbose_name='Data Cadastro')),
                ('updated', models.DateField(auto_now=True, verbose_name='Data Atualização')),
                ('discipulador', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Discipulador', to='pessoas.Pessoa')),
                ('lider', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Líder', to='pessoas.Pessoa')),
                ('predio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='predios.Predio', verbose_name='Prédio')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Supervisor', to='pessoas.Pessoa')),
            ],
        ),
    ]