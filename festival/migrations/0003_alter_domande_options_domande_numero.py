# Generated by Django 4.1.1 on 2023-09-08 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "festival",
            "0002_remove_domande_questionario_remove_domande_risposta_and_more",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="domande",
            options={"ordering": ["numero"]},
        ),
        migrations.AddField(
            model_name="domande",
            name="numero",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]