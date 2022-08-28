from django.core.cache import cache
from rest_framework.permissions import BasePermission
from .models import KoterConfiguration


class APIIsEnabled(BasePermission):
    CACHE_KEY = "koter:api_enabled"
    CACHE_TIME = 60 * 5  # 5 minutes

    def has_permission(self, request, view):
        enable_rest = cache.get(self.CACHE_KEY)

        if enable_rest is None:
            enable_rest = KoterConfiguration.current().enable_rest_api
            cache.set(self.CACHE_KEY, enable_rest, self.CACHE_TIME)

        return enable_rest
