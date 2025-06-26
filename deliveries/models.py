from typing import Any, Iterable
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from colorfield.fields import ColorField

from .validators import FileSizeValidator


class AbstractLabeledModel(models.Model):
    name = models.CharField(_("name"), max_length=50, unique=True)
    label = models.CharField(_("label"), max_length=50, blank=True, default="")

    description = models.TextField(_("description"), blank=True, default="")

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}:{self.pk}:{self.name}>"

    def __str__(self) -> str:
        return self.label or self.name

    class Meta:
        abstract = True


class Transport(AbstractLabeledModel):
    class Meta:
        verbose_name = _("Transport")
        verbose_name_plural = _("Transports")


class PackingType(AbstractLabeledModel):
    class Meta:
        verbose_name = _("Packing Type")
        verbose_name_plural = _("Packing Types")


class AdditionalService(AbstractLabeledModel):
    class Meta:
        verbose_name = _("Additional Service")
        verbose_name_plural = _("Additional Services")


class Status(AbstractLabeledModel):
    order = models.PositiveSmallIntegerField(
        _("order"),
        default=0,
        help_text=_(
            "Order of the status. Lower number means higher priority",
        ),
    )

    color = ColorField(
        _("color"),
        null=True,
        default=None,
        help_text=_("Color code in hex format"),
    )

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")
        ordering = ("order", "id")


class Delivery(models.Model):
    from_address = models.TextField(_("from address"))
    to_address = models.TextField(_("to address"))
    distance = models.PositiveIntegerField(_("distance"), help_text=_("in km"))

    from_datetime = models.DateTimeField(_("from datetime"))
    to_datetime = models.DateTimeField(_("to datetime"))

    transport = models.ForeignKey(
        Transport,
        on_delete=models.PROTECT,
        verbose_name=_("transport"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_("status"),
    )
    packing_type = models.ForeignKey(
        PackingType,
        on_delete=models.PROTECT,
        verbose_name=_("packing type"),
    )
    additional_services = models.ManyToManyField(
        AdditionalService,
        blank=True,
        verbose_name=_("additional services"),
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Delivery")
        verbose_name_plural = _("Deliveries")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._initial_status = self.status

    def save(self, *args, **kwargs) -> None:
        is_new_instance = self.pk is None
        initial_status = self._initial_status

        instance = super().save(*args, **kwargs)

        if is_new_instance or initial_status != self.status:
            DeliveryStatusHistory.objects.create(
                delivery=self,
                status=self.status,
            )

        self._initial_status = self.status
        return instance


class DeliveryStatusHistory(models.Model):
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        verbose_name=_("delivery"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name=_("status"),
    )

    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Delivery Status History")
        verbose_name_plural = _("Delivery Status Histories")


class DeliveryFile(models.Model):
    file = models.FileField(
        _("file"),
        upload_to="upload/",
        validators=[
            FileExtensionValidator(["pdf", "png", "jpg", "jpeg"]),
            FileSizeValidator(5),
        ],
        help_text=_("File related to the delivery"),
    )
    delivery = models.ForeignKey(
        Delivery,
        on_delete=models.CASCADE,
        verbose_name=_("delivery"),
    )

    class Meta:
        verbose_name = _("Delivery File")
        verbose_name_plural = _("Delivery Files")
