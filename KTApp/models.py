import uuid as uuid

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

from config_models.models import ConfigurationModel
from auditlog.registry import auditlog
from django_extensions.db.models import TimeStampedModel, ActivatorModel
from django_extensions.db.fields import AutoSlugField
from model_utils import FieldTracker

from auditlog.models import AuditlogHistoryField
from mirage import fields
from . import fields as kt_fields
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from address.models import AddressField, Address, Locality, State, Country

User = get_user_model()


class KoterConfiguration(TimeStampedModel, ConfigurationModel):
    enable_rest_api = models.BooleanField(_("Enable REST API"), default=False,
                                          help_text=_("Open Access Manager Rest API"))
    anonymize_rest_data = models.BooleanField(_("Anonymize REST data"), default=False, help_text=_(
        "This field will make all special data returned in API routes anonymized by default."))
    history = AuditlogHistoryField()

    def __str__(self):
        is_current = KoterConfiguration.current() == self
        return str(_("Current Config") if is_current else _("Old Config"))

    class Meta:
        verbose_name = _("Configuration")
        verbose_name_plural = _("Configurations")


class TaggedContact(TaggedItemBase):
    content_object = models.ForeignKey('KoterContact', on_delete=models.CASCADE)


def get_contact_id():
    return get_random_string(length=settings.KOTER_ID_LENGTH)


class KoterIntegration(TimeStampedModel, ActivatorModel):
    class Gateway(models.TextChoices):
        KOTER = "KTR", _("Köter")

    name = models.CharField(_("Name"), max_length=90, db_index=True)
    gateway = models.CharField(_("Gateway"), max_length=3, choices=Gateway.choices, unique=True)

    def __str__(self):
        return self.gateway


class KoterIntegrationUser(TimeStampedModel, ActivatorModel):
    integration = models.ForeignKey(KoterIntegration, verbose_name=_("Integration"), on_delete=models.CASCADE,
                                    db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True, verbose_name=_("User"))
    external_id = models.CharField(max_length=180, db_index=True, verbose_name=_("External ID"))

    def __str__(self):
        return self.user

    class Meta:
        verbose_name = _("Integration User")
        verbose_name_plural = _("Integration Users")


class KoterContact(TimeStampedModel):
    # Identification
    id = models.CharField(max_length=settings.KOTER_ID_LENGTH, default=get_contact_id, verbose_name=_("ID"),
                          primary_key=True, editable=False)
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name=_("UUID"), db_index=True, editable=False)
    # About
    first_name = fields.EncryptedCharField(max_length=180, blank=True, verbose_name=_("First name"))
    last_name = fields.EncryptedCharField(max_length=180, blank=True, verbose_name=_("Last name"))
    email = fields.EncryptedEmailField(blank=True, verbose_name=_("Email"))
    site = fields.EncryptedURLField(blank=True, verbose_name=_("Site"))
    address = AddressField(verbose_name=_("Address"), blank=True, null=True)

    ct_phone = kt_fields.EncryptedPhonenumberField(blank=True, verbose_name=_("Contact Phone"),
                                                   help_text=_("Phone number for sending SMS"))
    ct_whatsapp = kt_fields.EncryptedPhonenumberField(blank=True, verbose_name=_("Contact WhatsApp"),
                                                      help_text=_("Phone number registered on WhatsApp"))
    ct_telegram = kt_fields.EncryptedPhonenumberField(blank=True, verbose_name=_("Contact Telegram"),
                                                      help_text=_("Phone number registered on Telegram"))
    ct_facebook = fields.EncryptedURLField(blank=True, verbose_name=_("Facebook"))

    # Flags
    cbc = models.BooleanField(default=True, verbose_name=_("Can be contacted"),
                              help_text=_("User can be contacted (general)?"))
    cbc_email = models.BooleanField(default=True, verbose_name=_("Can be contacted by email"))
    cbc_sms = models.BooleanField(default=True, verbose_name=_("Can be contacted by sms"))
    cbc_whatsapp = models.BooleanField(default=True, verbose_name=_("Can be contacted by Whatsapp"))
    cbc_facebook = models.BooleanField(default=True, verbose_name=_("Can be contacted by Facebook"))
    cbc_telegram = models.BooleanField(default=True, verbose_name=_("Can be contacted by Telegram"))

    # Optin / Optout
    has_optin = models.BooleanField(default=False, verbose_name=_("Has optin"), help_text=_(
        "It is important that a contact has optin confirmation if they request information on how their data was obtained."))
    optin_date = models.DateTimeField(blank=True, verbose_name=_("Optin Date"), db_index=True, null=True)
    optin_details = models.TextField(blank=True, verbose_name=_("Optin Details"),
                                     help_text=_("Details on where and who opted in"))

    has_optout = models.BooleanField(default=False, verbose_name=_("Has optout"), help_text=_(
        "It is important to mark contacts with opt-out so that they do not receive new contacts from your company and thus avoid future problems."))
    optout_date = models.DateTimeField(blank=True, verbose_name=_("Optout Date"), db_index=True, null=True)
    optout_details = models.TextField(blank=True, verbose_name=_("Optin Details"),
                                      help_text=_("Details on where and who opted out"))

    tags = TaggableManager(through=TaggedContact, verbose_name=_("Tags"))
    history = AuditlogHistoryField()

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")


class KoterSegments(TimeStampedModel, ActivatorModel):
    class Meta:
        verbose_name = _("Segment")
        verbose_name_plural = _("Segments")

    name = models.CharField(_("Name"), max_length=80, db_index=True)
    description = models.TextField(verbose_name=_("Description"), blank=True)
    slug = AutoSlugField(populate_from='name')
    contacts = models.ManyToManyField(KoterContact, verbose_name=_("Contacts"), blank=True, db_index=True)

    # Segment Relational options
    tags = models.ManyToManyField(TaggedContact, verbose_name=_("Tags"), db_index=True, blank=True)
    localities = models.ManyToManyField(Locality, verbose_name=_("Locality"), db_index=True, blank=True)
    states = models.ManyToManyField(State, verbose_name=_("State"), db_index=True, blank=True)
    countries = models.ManyToManyField(Country, verbose_name=_("Countries"), db_index=True, blank=True)
    # Segment Boolean options
    cbc = models.BooleanField(default=None, verbose_name=_("Can be contacted"),
                              help_text=_("User can be contacted (general)?"), null=True)
    cbc_email = models.BooleanField(default=None, verbose_name=_("Can be contacted by email"), null=True)
    cbc_sms = models.BooleanField(default=None, verbose_name=_("Can be contacted by sms"), null=True)
    cbc_whatsapp = models.BooleanField(default=None, verbose_name=_("Can be contacted by Whatsapp"), null=True)
    cbc_facebook = models.BooleanField(default=None, verbose_name=_("Can be contacted by Facebook"), null=True)
    cbc_telegram = models.BooleanField(default=None, verbose_name=_("Can be contacted by Telegram"), null=True)

    # Flags
    need_refresh = models.BooleanField(default=True, verbose_name=_("Need a refresh"), editable=False)
    tracker = FieldTracker()

    # Audit
    history = AuditlogHistoryField()

    def __str__(self):
        return f"{self.name} ({self.contacts.count()} contacts)"

    def refresh_segment(self):
        qs_filter = {}

        if self.tags.count():
            qs_filter["tags__in"] = self.tags.all()
        if self.localities.count():
            qs_filter["address__locality__in"] = self.localities.all()
        if self.states.count():
            qs_filter["address__locality__state__in"] = self.states.all()
        if self.countries.count():
            qs_filter["address__locality__state__country__in"] = self.states.all()

        if self.cbc:
            qs_filter["cbc"] = self.cbc
        if self.cbc_email:
            qs_filter["cbc_email"] = self.cbc_email
        if self.cbc_sms:
            qs_filter["cbc_sms"] = self.cbc_sms
        if self.cbc_whatsapp:
            qs_filter["cbc_whatsapp"] = self.cbc_whatsapp
        if self.cbc_facebook:
            qs_filter["cbc_facebook"] = self.cbc_facebook
        if self.cbc_telegram:
            qs_filter["cbc_telegram"] = self.cbc_telegram

        qs = KoterContact.objects.filter(**qs_filter)
        self.contacts.set(qs)
        self.need_refresh = False

    def save(self, **kwargs):
        with self.tracker:
            if self.pk is None:
                super(KoterSegments, self).save(**kwargs)
            changed_dict = self.tracker.changed()
            if "modified" in changed_dict:
                del changed_dict["modified"]
            if self.need_refresh or len(changed_dict.keys()):
                self.refresh_segment()
            super(KoterSegments, self).save(**kwargs)


auditlog.register(KoterConfiguration)
auditlog.register(KoterContact)
auditlog.register(KoterSegments)
