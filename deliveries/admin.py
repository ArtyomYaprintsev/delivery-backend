from typing import Any
from django.contrib import admin
from django.http import HttpRequest

from .models import (
    Transport,
    PackingType,
    AdditionalService,
    Status,
    Delivery,
    DeliveryFile,
    DeliveryStatusHistory,
)


@admin.register(Transport)
class TransportAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "label")


@admin.register(PackingType)
class PackingTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "label")


@admin.register(AdditionalService)
class AdditionalServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "label")


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "label", "color")


class FileInline(admin.StackedInline):
    model = DeliveryFile
    extra = 0


class StatusHistoryInline(admin.TabularInline):
    model = DeliveryStatusHistory
    extra = 0

    fields = ("status", "created_at")
    readonly_fields = fields

    def has_add_permission(self, *args: Any, **kwargs: Any) -> bool:
        return False

    def has_change_permission(self, *args: Any, **kwargs: Any) -> bool:
        return False

    def has_delete_permission(self, *args: Any, **kwargs: Any) -> bool:
        return False


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    inlines = [FileInline, StatusHistoryInline]


@admin.register(DeliveryFile)
class DeliveryFileAdmin(admin.ModelAdmin):
    pass
