from django.contrib import admin
from django.urls import path
from .views import IndexPage

urlpatterns = [
    path("", IndexPage.as_view(), name="indexpage"),
]

