from rest_framework import serializers
from .models import TaggedContact, KoterContact, KoterSegments


class TaggedContactSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()
    tag_name = serializers.CharField(source="tag.name")

    def get_contacts(self, tagget_contact: TaggedContact):
        return TaggedContact.objects.filter(
            tag=tagget_contact.tag
        ).count()

    class Meta:
        model = TaggedContact
        fields = (
            'tag',
            "tag_name",
            "contacts",
        )