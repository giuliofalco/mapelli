# Generated by Django 3.2 on 2023-10-21 13:52

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openday', '0003_auto_20231021_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Indirizzi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=50)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='')),
                ('descrizione', ckeditor.fields.RichTextField()),
            ],
        ),
        migrations.AlterField(
            model_name='visitatori',
            name='nome',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.CreateModel(
            name='riga_orario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('materia', models.CharField(max_length=80)),
                ('prima', models.IntegerField(blank=True, null=True)),
                ('seconda', models.IntegerField(blank=True, null=True)),
                ('terza', models.IntegerField(blank=True, null=True)),
                ('quarta', models.IntegerField(blank=True, null=True)),
                ('quinta', models.IntegerField(blank=True, null=True)),
                ('indirizzo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='openday.indirizzi')),
            ],
        ),
    ]