# Generated by Django 3.2.11 on 2022-05-15 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pcto', '0006_auto_20220515_0608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abbinamenti',
            name='azienda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcto.aziende', to_field='partita_iva'),
        ),
    ]
