# Generated by Django 4.1 on 2022-08-27 02:50

import KTApp.fields
import KTApp.models
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import mirage.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('KTApp', '0002_remove_koterconfiguration_anonymize_database_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='KoterContact',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id', models.CharField(default=KTApp.models.get_contact_id, max_length=18, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='UUID')),
                ('first_name', mirage.fields.EncryptedCharField(blank=True, max_length=180, verbose_name='First name')),
                ('last_name', mirage.fields.EncryptedCharField(blank=True, max_length=180, verbose_name='Last name')),
                ('email', mirage.fields.EncryptedEmailField(blank=True, max_length=254, verbose_name='Email')),
                ('site', mirage.fields.EncryptedURLField(blank=True, verbose_name='Site')),
                ('ct_phone', KTApp.fields.EncryptedPhonenumberField(blank=True, help_text='Phone number for sending SMS', max_length=254, region=None, verbose_name='Contact Phone')),
                ('ct_whatsapp', KTApp.fields.EncryptedPhonenumberField(blank=True, help_text='Phone number registered on WhatsApp', max_length=254, region=None, verbose_name='Contact WhatsApp')),
                ('ct_telegram', KTApp.fields.EncryptedPhonenumberField(blank=True, help_text='Phone number registered on Telegram', max_length=254, region=None, verbose_name='Contact Telegram')),
                ('ct_facebook', mirage.fields.EncryptedURLField(blank=True, verbose_name='Facebook')),
                ('cbc', models.BooleanField(default=True, help_text='User can be contacted (general)?', verbose_name='Can be contacted')),
                ('cbc_email', models.BooleanField(default=True, verbose_name='Can be contacted by email')),
                ('cbc_sms', models.BooleanField(default=True, verbose_name='Can be contacted by sms')),
                ('cbc_whatsapp', models.BooleanField(default=True, verbose_name='Can be contacted by Whatsapp')),
                ('cbc_facebook', models.BooleanField(default=True, verbose_name='Can be contacted by Facebook')),
                ('cbc_telegram', models.BooleanField(default=True, verbose_name='Can be contacted by Telegram')),
                ('has_optin', models.BooleanField(default=False, help_text='It is important that a contact has optin confirmation if they request information on how their data was obtained.', verbose_name='Has optin')),
                ('optin_date', models.DateTimeField(blank=True, db_index=True, verbose_name='Optin Date')),
                ('optin_details', models.TextField(blank=True, help_text='Details on where and who opted in', verbose_name='Optin Details')),
                ('has_optout', models.BooleanField(default=False, help_text='It is important to mark contacts with opt-out so that they do not receive new contacts from your company and thus avoid future problems.', verbose_name='Has optout')),
                ('optout_date', models.DateTimeField(blank=True, db_index=True, verbose_name='Optout Date')),
                ('optout_details', models.TextField(blank=True, help_text='Details on where and who opted out', verbose_name='Optin Details')),
            ],
            options={
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.AlterModelOptions(
            name='koterconfiguration',
            options={'verbose_name': 'Configuration', 'verbose_name_plural': 'Configurations'},
        ),
        migrations.CreateModel(
            name='TaggedContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='KTApp.kotercontact')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='kotercontact',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='KTApp.TaggedContact', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
