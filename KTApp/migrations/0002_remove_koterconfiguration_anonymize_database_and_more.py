# Generated by Django 4.1 on 2022-08-27 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KTApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='koterconfiguration',
            name='anonymize_database',
        ),
        migrations.AddField(
            model_name='koterconfiguration',
            name='anonymize_rest_data',
            field=models.BooleanField(default=False, help_text='This field will make all special data returned in API routes anonymized by default.', verbose_name='Anonymize REST data'),
        ),
    ]