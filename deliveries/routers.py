from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):
    include_root_view = False
