from django.contrib import admin
from config_models.admin import ConfigurationModelAdmin
from django.db.models import QuerySet
from django.db import transaction

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (KoterConfiguration, KoterContact, KoterIntegrationUser, KoterSegments)


# Resources
class ContactResource(resources.ModelResource):
    class Meta:
        model = KoterContact


# Admin pages
@admin.register(KoterConfiguration)
class KoterConfigurationAdmin(ConfigurationModelAdmin):
    pass


@admin.register(KoterContact)
class KoterContactAdmin(ImportExportModelAdmin):
    resource_class = ContactResource

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ["id", "first_name", "last_name", "ct_phone", "email"]
        else:
            return ["first_name", "last_name"]


@admin.register(KoterIntegrationUser)
class KoterIntegrationUserAdmin(admin.ModelAdmin):
    raw_id_fields = ["user"]
    list_display = ["user", "external_id"]

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_or_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

@admin.action(description='Refresh segments')
def refresh_segment(modeladmin, request, queryset: QuerySet[KoterSegments]):
    with transaction.atomic():
        for item in queryset.filter(status=KoterSegments.ACTIVE_STATUS):
            item.need_refresh = True
            item.refresh_segment()


@admin.register(KoterSegments)
class KoterSegmentsAdmin(admin.ModelAdmin):
    actions = [refresh_segment]
    raw_id_fields = [
        'contacts',
        'tags',
        'localities',
        'states',
        'countries'
    ]


admin.site.site_header = 'Koter Mailing Manager'
