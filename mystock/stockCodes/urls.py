from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('stockCodes',views.stockCodes, name='stockCodes'),
]