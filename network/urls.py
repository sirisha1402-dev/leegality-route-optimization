from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    NodeViewSet,
    EdgeViewSet,
    RouteViewSet,
    RouteHistoryViewSet,
)

router = DefaultRouter()

router.register("nodes", NodeViewSet, basename="nodes")
router.register("edges", EdgeViewSet, basename="edges")
router.register("routes", RouteViewSet, basename="routes")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "routes/history/",
        RouteHistoryViewSet.as_view({"get": "list"}),
        name="route-history",
    ),
]