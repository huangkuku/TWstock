from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('revenue_profit',views.revenue_profit, name='revenue_profit'),
]