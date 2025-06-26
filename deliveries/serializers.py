from rest_framework import serializers

from .models import (
    Transport,
    PackingType,
    AdditionalService,
    Status,
    Delivery,
    DeliveryFile,
    DeliveryStatusHistory,
)


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = "__all__"


class PackingTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingType
        fields = "__all__"


class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class DeliveryFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFile
        fields = "__all__"
        extra_kwargs = {"file": {"use_url": False}}


class DeliveryStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryStatusHistory
        fields = "__all__"


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delivery
        fields = "__all__"


class CreateDeliverySerializer(DeliverySerializer):
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False,
        write_only=True,
    )

    def create(self, validated_data):
        files = validated_data.pop("files", [])
        instance = super().create(validated_data)

        if files and instance:
            for file in files:
                serializer = DeliveryFileSerializer(
                    data={"delivery": instance.pk, "file": file},
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance


class RetrieveDeliverySerializer(serializers.ModelSerializer):
    files = DeliveryFileSerializer(
        many=True,
        read_only=True,
        source="deliveryfile_set",
    )
    status_history = DeliveryStatusHistorySerializer(
        many=True,
        read_only=True,
        source="deliverystatushistory_set",
    )

    class Meta:
        model = Delivery
        fields = (
            "id",
            "from_address",
            "to_address",
            "distance",
            "from_datetime",
            "to_datetime",
            "created_at",
            "transport",
            "status",
            "status_history",
            "packing_type",
            "additional_services",
            "files",
        )
        read_only_fields = ("id", "status_history")
