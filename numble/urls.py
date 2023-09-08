from django.urls import path

from .views import index

urlpatterns = [
    path("<str:difficulty>/", index, name="index"),
]
