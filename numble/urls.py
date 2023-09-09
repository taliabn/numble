from django.urls import path

from .views import index, redirect_view

urlpatterns = [
    path("<str:difficulty>/", index, name="index"),
    path("", redirect_view, name="redirect_view"),
]
