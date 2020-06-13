from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('addapplication/<int:id>', views.application, name="application"),
]