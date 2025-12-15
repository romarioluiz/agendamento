from django.urls import path
from .views import optimize

urlpatterns = [
    path("optimize/", optimize),
]

