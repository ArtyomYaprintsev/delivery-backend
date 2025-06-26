from .routers import CustomRouter
from .views import (
    TransportViewSet,
    PackingTypeViewSet,
    AdditionalServiceViewSet,
    StatusViewSet,
    DeliveryViewSet,
    DeliveryFileViewSet,
)


router = CustomRouter()

router.register(r"", DeliveryViewSet, basename="delivery")
router.register(
    r"(?P<delivery_id>\d+)/files",
    DeliveryFileViewSet,
    basename="delivery-file",
)
router.register(r"transports", TransportViewSet, basename="transport")
router.register(r"packing-types", PackingTypeViewSet, basename="packing-type")
router.register(
    r"additional-services",
    AdditionalServiceViewSet,
    basename="additional-service",
)
router.register(r"statuses", StatusViewSet, basename="status")
