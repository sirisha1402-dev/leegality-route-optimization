from django.contrib import admin

from .models import Node, Edge, RouteHistory


@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Edge)
class EdgeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "source",
        "destination",
        "latency",
    ]


@admin.register(RouteHistory)
class RouteHistoryAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "source",
        "destination",
        "total_latency",
        "created_at",
    ]