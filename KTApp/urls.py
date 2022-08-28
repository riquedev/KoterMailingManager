from django.urls import path, include
from .views import admin_search, TaggedContactViewSet
from rest_framework import routers

app_name = "KT"

router = routers.DefaultRouter()
router.register(r'tags', TaggedContactViewSet)

urlpatterns = [
    path("search", admin_search, name="admin_search"),
    path("api/", include(router.urls), name="api")
]
