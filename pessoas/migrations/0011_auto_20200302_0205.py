# Generated by Django 3.0.1 on 2020-03-02 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0010_auto_20200229_0344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcaolideranca',
            name='categoria',
            field=models.CharField(choices=[('A', 'Apóstolo'), ('P', 'Pastor'), ('O', 'Obreiro'), ('D', 'Discipulador'), ('L', 'Líder'), ('T', 'Treinamento')], max_length=1),
        ),
    ]