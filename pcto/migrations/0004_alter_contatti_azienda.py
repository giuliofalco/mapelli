# Generated by Django 3.2.11 on 2022-04-22 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pcto', '0003_alter_contatti_azienda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contatti',
            name='azienda',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='pcto.aziende', to_field='partita_iva'),
        ),
    ]
