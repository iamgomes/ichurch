# Generated by Django 3.0.1 on 2019-12-29 20:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0003_auto_20191229_2036'),
        ('predios', '0002_predio_pastor'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='predio',
            options={'verbose_name_plural': 'Prédios'},
        ),
        migrations.AlterField(
            model_name='predio',
            name='pastor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pastor_do_predio', to='pessoas.Pessoa'),
        ),
    ]
