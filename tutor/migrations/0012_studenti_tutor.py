# Generated by Django 3.2 on 2023-10-08 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0011_alter_proposte_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='studenti',
            name='tutor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tutor.tutor'),
        ),
    ]