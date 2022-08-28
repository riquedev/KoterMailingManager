from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse

from .controller.ktapi import KTApi
from .utils import host_is_local, get_rest_permissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import APIException
from rest_framework_api_key.permissions import HasAPIKey
from .models import TaggedContact, KoterIntegrationUser
from .serializers import TaggedContactSerializer
from .permissions import APIIsEnabled


@staff_member_required
def admin_search(request):
    text = request.GET.get('text', None)
    res = [{
        "label": "Koter Configurations",
        "url": reverse("admin:KTApp_koterconfiguration_changelist"),
        "icon": "fa fa-cog"
    }]

    return JsonResponse({
        'length': len(res),
        'data': res
    })


def index(request):
    return JsonResponse({
        "version": settings.KOTER_VERSION,
        "secure": host_is_local(*request.get_host().split(":"))
    })


def redirect_log(request, filename):
    return redirect(to=reverse("log_viewer:log_file_view") + f"?file=json/{filename}")


class TaggedContactViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = get_rest_permissions()
    queryset = TaggedContact.objects.all().order_by('-id')
    serializer_class = TaggedContactSerializer

    def get_queryset(self):
        if self.headers.get(settings.KOTER_EXTERNAL_USER_ID, None) or self.request.user.is_authenticated:
            queryset = TaggedContact.objects.all().order_by('-id')
        else:
            KTApi.notify_insecure_request(self.request)
            raise APIException("This is an unsafe request, administrators have been notified.")
        return queryset
