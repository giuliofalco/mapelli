# Generated by Django 3.2 on 2023-10-17 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0017_alter_news_testo'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposte',
            name='allegato',
            field=models.URLField(blank=True, null=True),
        ),
    ]
