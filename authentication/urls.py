from django.urls import path

from .views import Login, Logout, UserMe


urlpatterns = [
    path(r"login/", Login.as_view()),
    path(r"logout/", Logout.as_view()),
    path(r"me/", UserMe.as_view()),
]
