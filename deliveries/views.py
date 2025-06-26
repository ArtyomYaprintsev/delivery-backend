from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _

from .models import Transport, PackingType, AdditionalService, Status, Delivery
from .serializers import (
    TransportSerializer,
    PackingTypeSerializer,
    AdditionalServiceSerializer,
    StatusSerializer,
    DeliverySerializer,
    CreateDeliverySerializer,
    RetrieveDeliverySerializer,
    DeliveryFileSerializer,
)


class TransportViewSet(ModelViewSet):
    queryset = Transport.objects.all()
    serializer_class = TransportSerializer


class PackingTypeViewSet(ModelViewSet):
    queryset = PackingType.objects.all()
    serializer_class = PackingTypeSerializer


class AdditionalServiceViewSet(ModelViewSet):
    queryset = AdditionalService.objects.all()
    serializer_class = AdditionalServiceSerializer


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class DeliveryViewSet(ModelViewSet):
    queryset = Delivery.objects.all()
    parser_classes = [MultiPartParser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateDeliverySerializer
        if self.action == "retrieve":
            return RetrieveDeliverySerializer
        return DeliverySerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class DeliveryFileViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = DeliveryFileSerializer

    def get_queryset(self):
        delivery_id = self.kwargs.get("delivery_id")

        if not delivery_id:
            raise APIException(
                detail=_("The `delivery_id` path parameter is required"),
                code=str(status.HTTP_400_BAD_REQUEST),
            )

        instance = Delivery.objects.filter(id=delivery_id).first()

        if instance is None:
            raise APIException(
                detail=_("The `Delivery` instance does not exist"),
                code=str(status.HTTP_404_NOT_FOUND),
            )

        return instance.deliveryfile_set.all()  # type: ignore
