# Generated by Django 3.2 on 2023-11-17 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0023_attivita_tutor_tipologia_attivita'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target_attivita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('etichetta', models.CharField(max_length=30)),
                ('descrizione', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
