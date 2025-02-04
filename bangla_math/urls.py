from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_dataset, name='show_dataset'),
]
