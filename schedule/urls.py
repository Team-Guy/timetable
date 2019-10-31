from django.contrib import admin
from django.urls import path
import schedule.views
urlpatterns = [
    path('', schedule.views.index),
]
