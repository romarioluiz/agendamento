# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('api/optimize/', views.optimize, name='optimize'),
]
