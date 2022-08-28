from phonenumber_field.modelfields import PhoneNumberField
from mirage.fields import EncryptedMixin


class EncryptedPhonenumberField(EncryptedMixin, PhoneNumberField):
    prepared_max_length = 254
